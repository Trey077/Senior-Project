from os import path
import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask.cli import load_dotenv
from sqlalchemy import text
from Flask_Application.Backend.Services.pipeline import process_and_store

from collections import defaultdict
import math



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
    #app configs to make launch easier
    app.config['MODEL_PATH'] = "Backend/models/Topic-Model"
    app.config['API_KEY'] = os.getenv('API_KEY')
    app.config['BASE_URL'] = "https://cpsideas.aha.io/api/v1/bookmarks/custom_pivots"
    app.config['ENDPOINT'] = "7433888668818238535"
    app.config['NUM_TOPICS'] = 13
    app.config['TOPIC_DOCS'] = [451, 210, 180, 163, 157, 137, 136, 120, 116, 112, 104, 92, 92]
    app.config['TEXT_COLUMN'] = "Description"
    app.config['TABLE_NAME'] = "Idea_Data"
    app.config['DATABASE_PATH'] = os.getenv('DATABASE_PATH')
    
    # Initialize the SQLAlchemy object with the Flask app
    db.init_app(app)


#data pipeline
    ''''
      with app.app_context():
       process_and_store(api_key=app.config['API_KEY'],
           base_url=app.config['BASE_URL'],
           endpoint=app.config['ENDPOINT'],
           model_path=app.config['MODEL_PATH'],
           num_topics=app.config['NUM_TOPICS'],
           topic_docs=app.config['TOPIC_DOCS'],
           db_path=app.config['DATABASE_PATH'],
           table_name=app.config['TABLE_NAME'],
         merge_column=app.config['TEXT_COLUMN']
      )
       '''



    # Define routes
    @app.route('/', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']

            if username == 'user' and password == 'password':
                flash('Login Successful!', 'success')
                return redirect(url_for('new_dashboard'))
            else:
                flash('Invalid username or password', 'danger')

        return render_template('login.html')

    @app.route('/logout')
    def logout():
            # Remove user session data
      session.pop('user_id', None)
      flash('You have logged out successfully.', 'success')  # Flash a success message
      return redirect(url_for('login'))  # Redirect to login page

        # Route to handle the Edit page for updating ideas

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
                            UPDATE Idea_Data
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
                result = db.session.execute(text("SELECT * FROM Idea_Data;")).fetchall()

                # Fetch distinct assigned_to values for the dropdown
                assignees_query = text("SELECT DISTINCT \"Assigned_to\" FROM Idea_Data")
                assignees_result = db.session.execute(assignees_query)
                assignees = [row[0] for row in assignees_result]  # Extract distinct assignees

                # Ensure valid rows were returned
                if not result:
                    flash("No ideas found in the database.", "warning")
                    return render_template('EditIdea.html', ideas=[], assignees=[])

                # Define column names to map the results to a dictionary
                column_names = ['Idea Reference', 'Name', 'Categories', 'Assigned_to', 'Status', 'Created_at', 'Votes',
                                'Tags', 'Description', 'Idea ID', 'Email']

                # Prepare a list of ideas to display in the dropdown
                ideas = []
                for row in result:
                    idea_data = {column_names[i]: row[i] for i in range(len(column_names))}
                    ideas.append(idea_data)

                # Prepare list of references and names for the dropdown
                dropdown_ideas = [{'reference': idea['Idea Reference'], 'name': idea['Name']} for idea in ideas]

                # Render the template and pass the ideas and assignees list
                return render_template('EditIdea.html', ideas=ideas, dropdown_ideas=dropdown_ideas, assignees=assignees)

            except Exception as e:
                print(f"Error: {e}")
                flash(f"Error accessing database: {e}", 'danger')  # Flash an error message if database access fails
                return f"Error accessing database: {e}"



    @app.route('/Merge Page')
    def merge_page():
        return render_template('Merge Page.html')

    @app.route('/new-dashboard', methods=['GET'])
    def new_dashboard():
        try:
            # Topic mapping: replace numbers with descriptive words
            topic_mapping = {
                0: "Patient Care and Safety",
                1: "Web Client and End Users",
                2: "Print/Scans",
                3: "Orders and Order Sets",
                4: "Medication Administration and Reconciliation",
                5: "Provider Services & Alerts",
                6: "Pharmacy and Perscription Workflow",
                7: "Billing and Charge Management",
                8: "Reports and Reporting Dashboard",
                9: "Search and Filteration Tools",
                10: "Notes and Documentation",
                11: "Lab Results and Clinical Monitoring",
                12: "Patient Scheduling and Processing"
            }

            # Fetch search query and selected tag
            search_query = request.args.get('search', '').strip().lower()
            selected_tag = request.args.get('tag', '').strip()

            # Fetch all columns from the 'Idea_Data' table
            result = db.session.execute(text("SELECT * FROM Idea_Data;")).fetchall()

            # Define the column names corresponding to your database table structure
            column_names = ['Idea Reference', 'Name', 'Categories', 'Assigned_to', 'Status', 'Created_at', 'Votes',
                            'Tags', 'Description', 'Idea ID', 'Email', 'Topic']

            # Convert the result into a list of dictionaries
            rows = []
            for row in result:
                row_data = {column_names[i]: row[i] for i in range(len(column_names))}
                rows.append(row_data)

            # Filter data based on search query and selected tag
            if search_query:
                rows = [row for row in rows if
                        search_query in row['Name'].lower() or search_query in row['Description'].lower()]
            if selected_tag:
                rows = [row for row in rows if selected_tag in row['Tags']]

            # Group the rows by mapped topic names
            grouped_ideas = defaultdict(list)
            for row in rows:
                topic_num = row.get('Topic')  # Assumes 'Topic' is a column in your database
                if topic_num is not None and topic_num in topic_mapping:
                    topic_word = topic_mapping[topic_num]
                    grouped_ideas[topic_word].append(row)

            # Fetch unique tags for filtering
            tags = db.session.execute(text("SELECT DISTINCT Tags FROM Idea_Data;")).fetchall()
            tags = [tag[0] for tag in tags]  # Convert result to a flat list

            # Render the template with grouped ideas and tags
            return render_template(
                'new-dashboard.html',
                grouped_ideas=grouped_ideas,
                search_query=search_query,
                selected_tag=selected_tag,
                tags=tags
            )

        except Exception as e:
            print(f"Error accessing database: {e}")
            return f"Error accessing database: {e}"

    # Temporary route for testing connection and displaying data
    @app.route('/test-database')
    def test_database():
        try:
            # Get the current page number from URL, default to 1 if not provided
            page = request.args.get('page', 1, type=int)
            per_page = 10  # Number of items per page

            # Get the search query and selected tag from the URL parameters
            search_query = request.args.get('search', '', type=str)
            selected_tag = request.args.get('tag', '', type=str)

            # Base SQL query to get ideas
            sql_query = "SELECT * FROM Idea_Data"

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
            tags_query = text("SELECT DISTINCT Tags FROM Idea_Data")
            tags_result = db.session.execute(tags_query)
            tags = [row[0] for row in tags_result]

            # Render the dashboard template with paginated rows, pagination data, and tags
            return render_template('test_database.html', rows=paginated_rows, page=page, total_pages=total_pages,
                                   search_query=search_query, tags=tags, selected_tag=selected_tag)

        except Exception as e:
            print(f"Error accessing database: {e}")
            flash(f"Error accessing database: {e}", 'danger')  # Flash an error message if there is an issue
            return f"Error accessing database: {e}"

    return app


