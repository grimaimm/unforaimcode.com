import os
from app import create_app
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = create_app()

if __name__ == "__main__":
    app.run(
        host=app.config.get("FLASK_RUN_HOST"),
        port=app.config.get("FLASK_RUN_PORT"),
    )