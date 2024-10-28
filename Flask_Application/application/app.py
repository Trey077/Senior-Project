from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('Dashboard.html')
@app.route('/Merge Page')
def merge_page():
    return render_template('Merge Page.html')

if __name__ == '__main__':
    app.run(debug=True)