import pytest
from app.utils import parse_resources, deduct_user_resources, update_metrics
from app.models import User, Resource, db, CommonMetric


@pytest.fixture
def sample_user(app):
    user = User(
        character_name="Test User", starting_resources="Time: 3, Money: 2, Labor: 1"
    )
    db.session.add(user)
    db.session.commit()
    return user


@pytest.fixture
def sample_resources(app, sample_user):
    resources = [
        Resource(type="Time", amount=3, user_id=sample_user.id),
        Resource(type="Money", amount=2, user_id=sample_user.id),
        Resource(type="Labor", amount=1, user_id=sample_user.id),
    ]
    db.session.bulk_save_objects(resources)
    db.session.commit()
    return resources


def test_parse_resources():
    resource_string = "Time: 3, Money: 2, Labor: 1"
    expected_output = {"Time": 3, "Money": 2, "Labor": 1}
    assert parse_resources(resource_string) == expected_output


def test_deduct_user_resources(app, sample_user, sample_resources):
    contributions = {"Time": 2, "Money": 1, "Labor": 1}
    deduct_user_resources(sample_user, contributions)
    updated_resources = {res.type: res.amount for res in sample_user.resources}
    assert updated_resources["Time"] == 1
    assert updated_resources["Money"] == 1
    assert updated_resources["Labor"] == 0


def test_update_metrics(app):
    metric = CommonMetric(type="Environment", value=5)
    db.session.add(metric)
    db.session.commit()
    update_metrics("Environment: +3, Economy: +2", None)
    updated_metric = CommonMetric.query.filter_by(type="Environment").first()
    assert updated_metric.value == 8
