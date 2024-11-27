# attempting to define functions to call each column for use in html 9pm 11-24-24
from . import create_app, db
from sqlalchemy import text

# Fetch 'Idea Reference' column
def get_idea_reference():
    try:
        result = db.session.execute(text("SELECT `Idea Reference` FROM Idea_Database;")).fetchall()
        return [row[0] for row in result]
    except Exception as e:
        print(f"Error fetching 'Idea Reference': {e}")
        return []

# Fetch 'Name' column
def get_name():
    try:
        result = db.session.execute(text("SELECT `Name` FROM Idea_Database;")).fetchall()
        return [row[0] for row in result]
    except Exception as e:
        print(f"Error fetching 'Name': {e}")
        return []

# Fetch 'Categories' column
def get_categories():
    try:
        result = db.session.execute(text("SELECT `Categories` FROM Idea_Database;")).fetchall()
        return [row[0] for row in result]
    except Exception as e:
        print(f"Error fetching 'Categories': {e}")
        return []

# Fetch 'Assigned_to' column
def get_assigned_to():
    try:
        result = db.session.execute(text("SELECT `Assigned_to` FROM Idea_Database;")).fetchall()
        return [row[0] for row in result]
    except Exception as e:
        print(f"Error fetching 'Assigned_to': {e}")
        return []

# Fetch 'Status' column
def get_status():
    try:
        result = db.session.execute(text("SELECT `Status` FROM Idea_Database;")).fetchall()
        return [row[0] for row in result]
    except Exception as e:
        print(f"Error fetching 'Status': {e}")
        return []

# Fetch 'Created_at' column
def get_created_at():
    try:
        result = db.session.execute(text("SELECT `Created_at` FROM Idea_Database;")).fetchall()
        return [row[0] for row in result]
    except Exception as e:
        print(f"Error fetching 'Created_at': {e}")
        return []

# Fetch 'Votes' column
def get_votes():
    try:
        result = db.session.execute(text("SELECT `Votes` FROM Idea_Database;")).fetchall()
        return [row[0] for row in result]
    except Exception as e:
        print(f"Error fetching 'Votes': {e}")
        return []

# Fetch 'Tags' column
def get_tags():
    try:
        result = db.session.execute(text("SELECT `Tags` FROM Idea_Database;")).fetchall()
        return [row[0] for row in result]
    except Exception as e:
        print(f"Error fetching 'Tags': {e}")
        return []

# Fetch 'Description' column
def get_description():
    try:
        result = db.session.execute(text("SELECT `Description` FROM Idea_Database;")).fetchall()
        return [row[0] for row in result]
    except Exception as e:
        print(f"Error fetching 'Description': {e}")
        return []

# Fetch 'Idea ID' column
def get_idea_id():
    try:
        result = db.session.execute(text("SELECT `Idea ID` FROM Idea_Database;")).fetchall()
        return [row[0] for row in result]
    except Exception as e:
        print(f"Error fetching 'Idea ID': {e}")
        return []

# Fetch 'Email' column
def get_email():
    try:
        result = db.session.execute(text("SELECT `Email` FROM Idea_Database;")).fetchall()
        return [row[0] for row in result]
    except Exception as e:
        print(f"Error fetching 'Email': {e}")
        return []
