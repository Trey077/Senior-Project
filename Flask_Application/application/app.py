from flask import Flask, render_template, request, redirect, url_for, flash
import os

from flask.cli import load_dotenv

load_dotenv()

api_key = os.getenv("API_KEY")

app = Flask(__name__)

@app.route('/login')
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == 'user' and password == 'password':
            flash('Login Successful!', 'success')
            return redirect(url_for('Dashboard'))
        else:
            flash('Invalid username or password', 'danger')

    return render_template('login.html')




@app.route('/')
def home():
    return render_template('Dashboard.html')
@app.route('/Merge Page')
def merge_page():
    return render_template('Merge Page.html')

if __name__ == '__main__':
    app.run(debug=True)