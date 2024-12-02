from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask.cli import load_dotenv
from sqlalchemy import text
import os
import math

# Load environment variables from a .env file
load_dotenv()

# Get the API key from environment variables (if needed)
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

    @app.route('/Merge', methods=['GET', 'POST'])
    def merge_page():
        try:
            # Fetch all columns from the 'Idea_Database' table
            result = db.session.execute(text("SELECT * FROM Idea_Database;")).fetchall()

            # Convert the result into a list of dictionaries for easier access in the template
            column_names = ['Idea Reference', 'Name', 'Categories', 'Assigned_to', 'Status', 'Created_at', 'Votes',
                            'Tags', 'Description', 'Idea ID', 'Email']
            ideas = []
            for row in result:
                row_data = {column_names[i]: row[i] for i in range(len(column_names))}
                ideas.append(row_data)

            # Handle form submission for merging
            if request.method == 'POST':
                main_idea_id = request.form['main_idea']
                secondary_idea_id = request.form['secondary_idea']

                # Fetch the selected main idea and secondary idea from the database
                main_idea = next((idea for idea in ideas if idea['Idea Reference'] == main_idea_id), None)
                secondary_idea = next((idea for idea in ideas if idea['Idea Reference'] == secondary_idea_id), None)

                if main_idea and secondary_idea:
                    # Merge the two ideas: keep main idea's columns and add secondary idea's Description, Tags, Email
                    main_idea['Description'] = secondary_idea['Description']
                    main_idea['Tags'] = secondary_idea['Tags']
                    main_idea['Email'] = secondary_idea['Email']

                    # Redirect to a new page showing the updated main idea
                    return render_template('merged_result.html', idea=main_idea)

            return render_template('MergePage.html', ideas=ideas)
        except Exception as e:
            print(f"Error: {e}")
            return f"Error accessing database: {e}"

    # Route for testing database with pagination
    @app.route('/')
    def test_database():
        try:
            # Get the current page from the URL query parameter, default to page 1
            page = request.args.get('page', 1, type=int)
            per_page = 10  # Set how many items to show per page

            # Fetch all columns from the 'Idea_Database' table
            result = db.session.execute(text("SELECT * FROM Idea_Database;")).fetchall()
            # Convert the result into a list of dictionaries for easier access in the template
            column_names = ['Idea Reference', 'Name', 'Categories', 'Assigned_to', 'Status', 'Created_at', 'Votes',
                            'Tags', 'Description', 'Idea ID', 'Email']
            rows = []
            for row in result:
                row_data = {column_names[i]: row[i] for i in range(len(column_names))}
                rows.append(row_data)

            # Pagination: Calculate total pages
            total_ideas = len(rows)
            total_pages = math.ceil(total_ideas / per_page)

            # Slice the rows for the current page
            start = (page - 1) * per_page
            end = start + per_page
            paginated_rows = rows[start:end]

            # Render the template with paginated rows and pagination data
            return render_template('test_database.html', rows=paginated_rows, page=page, total_pages=total_pages)

        except Exception as e:
            print(f"Error accessing database: {e}")
            return f"Error accessing database: {e}"

    return app
