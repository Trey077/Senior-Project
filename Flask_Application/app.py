from flask import Flask, render_template, request, redirect, url_for, flash
import os
from application import create_app, db
from flask.cli import load_dotenv
from sqlalchemy import text

load_dotenv()

api_key = os.getenv("API_KEY")

app = create_app()
"""
# Test database connection and access
with app.app_context():
    try:
        result = db.session.execute(text('SELECT * FROM Idea_Database')).fetchall()
        for row in result:
            print(row)
    except Exception as e:
        print(f"Error accessing the database: {e}")"""

if __name__ == '__main__':
    app.run(debug=True)
