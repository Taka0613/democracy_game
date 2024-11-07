import pytest
from flask import url_for
from app.models import User, Project, db


@pytest.fixture
def sample_project(app):
    project = Project(
        name="Test Project",
        description="Test Description",
        outcomes="Environment: +2, Welfare: +1",
        required_resources="Time: 2, Money: 1",
    )
    db.session.add(project)
    db.session.commit()
    return project


def test_login_route(client, app):
    response = client.get(url_for("main.login"))
    assert response.status_code == 200
    assert b"Login" in response.data


def test_dashboard_route(client, app, sample_user):
    client.post(
        url_for("main.login"), data={"character_name": sample_user.character_name}
    )
    response = client.get(url_for("main.dashboard"))
    assert response.status_code == 200
    assert b"Dashboard" in response.data


def test_project_detail_route(client, app, sample_project, sample_user):
    client.post(
        url_for("main.login"), data={"character_name": sample_user.character_name}
    )
    response = client.get(url_for("main.project_detail", project_id=sample_project.id))
    assert response.status_code == 200
    assert b"Test Project" in response.data
