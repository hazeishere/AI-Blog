# AI Blog Generator

A fun web application that generates humorous and entertaining blog posts using AI. Users submit a topic, and the AI automatically creates a witty title and generates a full blog post in markdown format.

## Features

- Simple web interface to create new blog posts
- AI-generated witty titles based on user-provided topics
- AI-generated entertaining content with a casual, humorous tone
- Markdown rendering with support for code blocks, tables, and lists
- Responsive design
- SQLite database for storing posts
- Post deletion functionality

## Setup and Installation

1. Clone this repository
2. Create and activate a virtual environment (recommended):
   ```
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Set up environment variables:
   - Create a `.env` file in the project root with the following:
     ```
     SECRET_KEY=your_secret_key_here
     DATABASE_PATH=blog.db
     DEBUG=True
     ```
5. Run the application:
   ```
   python app.py
   ```
6. Open your browser and navigate to `http://127.0.0.1:5002`

## Usage

1. Click "Create New Post" on the homepage
2. Enter a topic for your blog post
3. Click "Generate Blog Post"
4. Wait a few seconds for the AI to generate content
5. Once complete, you'll be redirected to view your new post
6. You can delete posts from the view page

## How It Works

1. When a user submits a topic, the app first generates a witty title using GPT-4o
2. Then it uses the title and topic to generate a full blog post with:
   - A casual, humorous introduction
   - Relaxed and conversational tone
   - Pop culture references or analogies
   - Witty observations related to the topic
   - Personal anecdotes or relatable scenarios
   - Interesting facts presented in a fun way
   - A lighthearted conclusion