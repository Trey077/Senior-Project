from os import path
import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask.cli import load_dotenv
from sqlalchemy import text

# Load environment variables from a .env file
load_dotenv()

# Get the API key from environment variables
api_key = os.getenv("API_KEY")

# Initialize the SQLAlchemy object
db = SQLAlchemy()
DB_NAME = os.path.abspath(os.getenv('DATABASE_PATH'))
print(f"Resolved database path: {DB_NAME}")

def create_app():
    # Create a Flask application instance
    app = Flask(__name__)

    # Set the secret key for session management
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    # Set the database URI for SQLAlchemy
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    
    # Initialize the SQLAlchemy object with the Flask app
    db.init_app(app)

    # Define routes
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']

            if username == 'user' and password == 'password':
                flash('Login Successful!', 'success')
                return redirect(url_for('home'))
            else:
                flash('Invalid username or password', 'danger')

        return render_template('login.html')

    @app.route('/')
    def home():
        return render_template('Dashboard.html')

    @app.route('/Merge Page')
    def merge_page():
        return render_template('Merge Page.html')

    # Temporary route for testing connection and displaying data
    @app.route('/test-database')
    def test_database():
        try:
            # Fetch all columns from the 'Idea_Database' table
            result = db.session.execute(text("SELECT * FROM Idea_Database;")).fetchall()

            # Convert the result into a list of dictionaries for easier access in the template
            column_names = ['Idea Reference', 'Name', 'Categories', 'Assigned_to', 'Status', 'Created_at', 'Votes',
                            'Tags', 'Description', 'Idea ID', 'Email']
            rows = []
            for row in result:
                row_data = {column_names[i]: row[i] for i in range(len(column_names))}
                rows.append(row_data)

            return render_template('test_database.html', rows=rows)
        except Exception as e:
            print(f"Error accessing database: {e}")
            return f"Error accessing database: {e}"



    return app


