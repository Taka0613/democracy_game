import pytest
import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
from app.models import User, Resource, db


def test_user_creation(app):
    user = User(
        character_name="Test Character",
        interests="Testing interests",
        utility_criteria="Testing criteria",
        starting_resources="Time: 3, Money: 2, Labor: 1",
    )
    db.session.add(user)
    db.session.commit()
    assert user.id is not None


def test_resource_assignment(app, sample_user):
    resource = Resource(type="Time", amount=5, user_id=sample_user.id)
    db.session.add(resource)
    db.session.commit()
    assert resource.user_id == sample_user.id
    assert sample_user.resources[0].type == "Time"
    assert sample_user.resources[0].amount == 5
