import os

from flask.cli import load_dotenv

from application import create_app

load_dotenv()

api_key = os.getenv("API_KEY")

app = create_app()


if __name__ == '__main__':
    app.run(debug=True)
