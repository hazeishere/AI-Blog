# AI Tech Blog

A web application that generates technology blog posts using AI. Users submit a title, and the AI automatically generates a full blog post in markdown format.

## Features

- Simple web interface to create new blog posts
- AI-generated content based on title inputs
- Markdown rendering for proper formatting of posts
- Responsive design with Bootstrap
- Syntax highlighting for code blocks

## Setup and Installation

1. Clone this repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the application:
   ```
   cd ai-blog
   python app.py
   ```
4. Open your browser and navigate to `http://127.0.0.1:5000`

## Usage

1. Click "Create New Post" on the homepage
2. Enter a title for your tech blog post
3. Click "Generate Blog Post"
4. Wait a few seconds for the AI to generate content
5. Once complete, you'll be redirected to view your new post

## Dependencies

- Flask: Web framework
- g4f: AI content generation
- Markdown: Converting markdown to HTML
- Bootstrap: Frontend styling
- Highlight.js: Code syntax highlighting 