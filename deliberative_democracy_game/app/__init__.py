# app/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_socketio import SocketIO
from config import Config

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
socketio = SocketIO()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize app with extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "main.login"  # Ensure it matches the Blueprint's route
    socketio.init_app(app)

    # Import models, utils, and register Blueprint
    with app.app_context():
        from . import (
            models,
            utils,
        )  # Import models and utils (to ensure they're registered)
        from .routes import main  # Import the Blueprint

        app.register_blueprint(main)  # Register the Blueprint for routes

        # Create database tables if they don't exist
        db.create_all()

    return app
