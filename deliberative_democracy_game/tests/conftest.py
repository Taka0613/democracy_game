# tests/conftest.py
import pytest
import sys
import os

# Add the project root to the Python path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
)  # Corrected the closing parenthesis

from app import create_app, db


@pytest.fixture(scope="module")
def app():
    """Create and configure a new app instance for each test module."""
    app = create_app()
    app.config.update(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        }
    )

    with app.app_context():
        db.create_all()  # Create tables for the test
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture(scope="module")
def client(app):
    """A test client for the app."""
    return app.test_client()


@pytest.fixture(scope="module")
def sample_user(app):
    """A sample user fixture for testing."""
    from app.models import User

    user = User(
        character_name="Test User",
        interests="Testing interests",
        utility_criteria="Test criteria",
    )
    db.session.add(user)
    db.session.commit()
    return user


@pytest.fixture(scope="module")
def sample_project(app):
    """A sample project fixture for testing."""
    from app.models import Project

    project = Project(
        name="Test Project",
        description="Test description",
        required_resources="Time: 2, Money: 1",
    )
    db.session.add(project)
    db.session.commit()
    return project
