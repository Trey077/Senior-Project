from flask import Flask, render_template, request, redirect, url_for, flash
import os
from application import create_app
from flask.cli import load_dotenv

load_dotenv()

api_key = os.getenv("API_KEY")

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)