from flask import Flask, request, redirect, url_for, flash, jsonify, session, render_template
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
DB_NAME = os.path.abspath(os.getenv('DATABASE_PATH'))  # Get the absolute path of the database
print(f"Resolved database path: {DB_NAME}")

# Function to create the Flask app
def create_app():
    # Create a Flask application instance
    app = Flask(__name__)

    # Set the secret key for session management
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'  # Replace with a secure secret key in production

    # Set the database URI for SQLAlchemy to connect to the SQLite database
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

    # Initialize the SQLAlchemy object with the Flask app
    db.init_app(app)

    # Define routes for the app
    # Route for user login
    @app.route('/', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form['username']  # Get the username from the form
            password = request.form['password']  # Get the password from the form

            # Check if the username and password match
            if username == 'user' and password == 'password':
                flash('Login Successful!', 'success')  # Flash a success message
                return redirect(url_for('test_database'))  # Redirect to the database test page
            else:
                flash('Invalid username or password', 'danger')  # Flash an error message for invalid credentials

        # Render the login page
        return render_template('login.html')

    # Route for logging out
    @app.route('/logout')
    def logout():
        # Remove user session data
        session.pop('user_id', None)
        flash('You have logged out successfully.', 'success')  # Flash a success message
        return redirect(url_for('login'))  # Redirect to login page

    # Route to handle the Edit page for updating ideas
    @app.route('/Edit', methods=['GET', 'POST'])
    def edit_page():
        if request.method == 'POST':
            # Get the form data to update the idea
            idea_reference = request.form['Idea Reference']
            name = request.form['Name']
            categories = request.form['Categories']
            assigned_to = request.form['Assigned_to']
            status = request.form['Status']
            created_at = request.form['Created_at']
            votes = request.form['Votes']
            tags = request.form['Tags']
            description = request.form['Description']
            idea_id = request.form['Idea ID']
            email = request.form['Email']

            try:
                # SQL query to update the idea in the database
                db.session.execute(
                    text(""" 
                        UPDATE Idea_Database
                        SET 
                            "Name" = :name,
                            "Categories" = :categories,
                            "Assigned_to" = :assigned_to,
                            "Status" = :status,
                            "Created_at" = :created_at,
                            "Votes" = :votes,
                            "Tags" = :tags,
                            "Description" = :description,
                            "Email" = :email
                        WHERE "Idea ID" = :idea_id
                    """),
                    {
                        'name': name,
                        'categories': categories,
                        'assigned_to': assigned_to,
                        'status': status,
                        'created_at': created_at,
                        'votes': votes,
                        'tags': tags,
                        'description': description,
                        'email': email,
                        'idea_id': idea_id
                    }
                )
                db.session.commit()  # Commit the changes to the database
                flash('Idea Updated Successfully', 'success')  # Flash a success message
                return redirect(url_for('edit_page'))  # Redirect to the same edit page
            except Exception as e:
                db.session.rollback()  # Rollback in case of error
                flash(f'Error updating idea: {e}', 'danger')  # Flash an error message
                return redirect(url_for('edit_page'))

        try:
            # Fetch all columns from the 'Idea_Database' table
            result = db.session.execute(text("SELECT * FROM Idea_Database;")).fetchall()

            # Print the result for debugging
            print(f"Fetched rows: {result}")

            # Ensure valid rows were returned
            if not result:
                flash("No ideas found in the database.", "warning")
                return render_template('EditIdea.html', ideas=[])

            # Define column names to map the results to a dictionary
            column_names = ['Idea Reference', 'Name', 'Categories', 'Assigned_to', 'Status', 'Created_at', 'Votes',
                            'Tags', 'Description', 'Idea ID', 'Email']

            # Prepare a list of ideas to display in the dropdown
            ideas = []
            for row in result:
                idea_data = {column_names[i]: row[i] for i in range(len(column_names))}
                ideas.append(idea_data)

            # Prepare list of references and names for dropdown
            dropdown_ideas = [{'reference': idea['Idea Reference'], 'name': idea['Name']} for idea in ideas]

            # Render the template and pass the ideas and dropdown list
            return render_template('EditIdea.html', ideas=ideas, dropdown_ideas=dropdown_ideas)

        except Exception as e:
            print(f"Error: {e}")
            flash(f"Error accessing database: {e}", 'danger')  # Flash an error message if database access fails
            return f"Error accessing database: {e}"

    # Route to test database and display ideas with pagination
    @app.route('/Dashboard', methods=['GET', 'POST'])
    def test_database():
        try:
            # Get the current page number from URL, default to 1 if not provided
            page = request.args.get('page', 1, type=int)
            per_page = 10  # Number of items per page

            # Get the search query and selected tag from the URL parameters
            search_query = request.args.get('search', '', type=str)
            selected_tag = request.args.get('tag', '', type=str)

            # Base SQL query to get ideas
            sql_query = "SELECT * FROM Idea_Database"

            # Add conditions for search query or selected tag
            conditions = []
            if search_query:
                conditions.append(f'"Name" LIKE :search_query OR "Description" LIKE :search_query')
            if selected_tag:
                conditions.append(f'"Tags" LIKE :selected_tag')

            # Combine conditions into the SQL query
            if conditions:
                sql_query += " WHERE " + " AND ".join(conditions)

            # Execute the query with parameters
            query = text(sql_query)
            result = db.session.execute(query, {
                'search_query': f'%{search_query}%' if search_query else None,
                'selected_tag': f'%{selected_tag}%' if selected_tag else None
            })

            # Convert the result into a list of dictionaries for easier use in the template
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

            # Fetch all unique tags for the dropdown
            tags_query = text("SELECT DISTINCT Tags FROM Idea_Database")
            tags_result = db.session.execute(tags_query)
            tags = [row[0] for row in tags_result]

            # Render the dashboard template with paginated rows, pagination data, and tags
            return render_template('Dashboard.html', rows=paginated_rows, page=page, total_pages=total_pages,
                                   search_query=search_query, tags=tags, selected_tag=selected_tag)

        except Exception as e:
            print(f"Error accessing database: {e}")
            flash(f"Error accessing database: {e}", 'danger')  # Flash an error message if there is an issue
            return f"Error accessing database: {e}"

    # Return the Flask app instance to be run
    return app
