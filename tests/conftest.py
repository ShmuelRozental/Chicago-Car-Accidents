import os
import sys

import pytest
from dotenv import load_dotenv
from flask import Flask

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from routes.querys_routes import queries_bp
from routes.insert_routes import accident_bp

load_dotenv()

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config.from_object('config.Config')


    app.register_blueprint(accident_bp)
    app.register_blueprint(queries_bp)

    return app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    from pymongo.errors import ServerSelectionTimeoutError
    from dal.connect import database

    try:
        database.client.admin.command("ping")
    except ServerSelectionTimeoutError as e:
        pytest.exit(f"Error connecting to the database: {e}")
