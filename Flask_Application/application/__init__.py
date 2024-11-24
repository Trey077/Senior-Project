from os import path
import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask.cli import load_dotenv
from sqlalchemy import text
import shutil

# Load environment variables from a .env file
load_dotenv()

# Get the API key from environment variables
api_key = os.getenv("API_KEY")

# Initialize the SQLAlchemy object
db = SQLAlchemy()
#DB_NAME = "../notebooks/persistent_database.sqlite"
DB_NAME = os.getenv('DATABASE_PATH', '../notebooks/persistent_database.sqlite')


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

    #temp route for testing connection
    @app.route('/test-database')
    def test_database():
        try:
            results = db.session.execute(text('SELECT * FROM Idea_Database')).fetchall()
            return render_template('test_database.html', results=results)
        except Exception as e:
            return f"Error accessing database: {e}"

    # Create the database tables if they do not exist
    with app.app_context():
        db.create_all()

    return app
#original attempt to make sql database
def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')


