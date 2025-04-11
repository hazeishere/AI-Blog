from flask import Flask, render_template, request, redirect, url_for, flash
import g4f
import sqlite3
import os
import markdown
from datetime import datetime
from dotenv import load_dotenv

# Get the directory where the app.py file is located
base_dir = os.path.dirname(os.path.abspath(__file__))

# Load environment variables
load_dotenv(os.path.join(base_dir, '.env'))

# Create app with the correct template folder
template_dir = os.path.join(base_dir, 'templates')
static_dir = os.path.join(base_dir, 'static')
app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
app.secret_key = os.getenv('SECRET_KEY', 'default_secret_key')

# Define database path
db_name = os.getenv('DATABASE_PATH')
DB_PATH = os.path.join(base_dir, db_name)

# Ensure the templates and static directories exist
os.makedirs(template_dir, exist_ok=True)
os.makedirs(static_dir, exist_ok=True)

# Pass current year to all templates
@app.context_processor
def inject_current_year():
    return {'current_year': datetime.now().year}

# Database setup
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Enable foreign keys
    cursor.execute("PRAGMA foreign_keys = ON")
    
    # Increase SQLite page size and cache size for better handling of large text
    cursor.execute("PRAGMA page_size = 4096")
    cursor.execute("PRAGMA cache_size = 10000")
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS posts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        content TEXT NOT NULL,  -- SQLite TEXT can store large content
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    conn.commit()
    conn.close()

# Initialize the database on startup
init_db()

# AI content generation function
def generate_content(title):
    prompt = f"""Write a detailed technology blog post about "{title}".
    Include the following:
    - An engaging introduction that explains the importance of this topic
    - Organized sections with proper headings (use Markdown formatting)
    - Technical details and examples where appropriate
    - Future implications and trends
    - A conclusion summarizing key points
    
    Format the entire post in proper Markdown with headings, bullet points, and code blocks as needed.
    IMPORTANT: Ensure your response is complete and well-structured, with no sentences cut off midway, and word count should be between 1500 and 2500 words.
    """
    
    try:
        # Using g4f to generate content
        response = g4f.ChatCompletion.create(
            model="claude-3.7-sonnet",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=4000  # Ensure we get a complete response
        )
        
        # Make sure the response is not cut off at the end
        if response and not response.endswith(('.', '!', '?', ':', '"', "'", ')', ']', '}')):
            # If it seems like it might be cut off, add an ellipsis to indicate that
            response += "..."
            
        return response
    except Exception as e:
        print(f"Error generating content: {e}")
        return None

# Routes
@app.route('/')
def index():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, created_at FROM posts ORDER BY created_at DESC")
    posts = cursor.fetchall()
    conn.close()
    return render_template('index.html', posts=posts)

@app.route('/post/<int:post_id>')
def view_post(post_id):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM posts WHERE id = ?", (post_id,))
    post = cursor.fetchone()
    conn.close()
    
    if post:
        # Convert markdown to HTML with extended support
        content_html = markdown.markdown(
            post['content'], 
            extensions=[
                'markdown.extensions.fenced_code',
                'markdown.extensions.tables',
                'markdown.extensions.nl2br',  # Convert newlines to line breaks
                'markdown.extensions.sane_lists'  # Better list handling
            ]
        )
        return render_template('post.html', post=post, content_html=content_html)
    else:
        flash('Post not found')
        return redirect(url_for('index'))

@app.route('/new', methods=['GET', 'POST'])
def new_post():
    if request.method == 'POST':
        title = request.form.get('title')
        if not title:
            flash('Title is required!')
            return redirect(url_for('new_post'))
        
        # Generate content using AI
        content = generate_content(title)
        if not content:
            flash('Failed to generate content. Please try again.')
            return redirect(url_for('new_post'))
        
        # Save to database
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
                    (title, content))
        post_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        flash('Post created successfully!')
        return redirect(url_for('view_post', post_id=post_id))
    
    return render_template('new_post.html')

if __name__ == '__main__':
    app.run(debug=os.getenv('DEBUG', 'False').lower() in ('true', '1', 't'), port=5001)
