A clean, responsive blogging platform built with Python and Django. This project is designed to be lightweight, using SQLite for easy portability and development.

🚀 Features
Post Management: Create, update, and delete blog entries.

User Authentication: Secure login/logout functionality for authors.

Database: Powered by SQLite for zero-configuration setup.

Responsive Design: Fully accessible on mobile and desktop devices.

🛠️ Technical Stack
Backend: Django 5.x

Language: Python 3.x

Database: SQLite

Editor: VS Code (Recommended)

💻 Getting Started
Prerequisites
Ensure you have Python installed on your machine. You can check by running:

Bash
python --version
Installation
Clone the repository:

Bash
git clone https://github.com/yourusername/maddyblog.git
cd maddyblog
Create a Virtual Environment:

Bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install Dependencies:

Bash
pip install django
Database Setup
Since this project uses SQLite, the database is a simple file within your project structure. Run the migrations to initialize the schema:

Bash
python manage.py migrate
Running the Server
Start the development server with:

Bash
python manage.py runserver
Navigate to http://127.0.0.1:8000/ in your browser to view the blog.

📂 Project Structure
Plaintext
maddyblog/
├── maddyblog/         # Project configuration
├── blog/              # Main application logic (models, views, templates)
├── manage.py          # Django command-line utility
└── db.sqlite3         # SQLite database file
