# app/utils.py

from .models import db, CommonMetric


def parse_resources(resource_string):
    """
    Parse a resource string like 'Time: 2, Money: 1' and return a dictionary.
    """
    resource_dict = {}
    resources = resource_string.split(", ")
    for resource in resources:
        if ": " in resource:
            key, value = resource.split(": ")
            resource_dict[key.lower()] = int(value)
    return resource_dict


def check_contributions(contributions, required_resources):
    """
    Check if contributions meet or exceed the required resources.
    """
    for resource, required_amount in required_resources.items():
        contributed_amount = contributions.get(resource, 0)
        if contributed_amount < required_amount:
            return "not enough"
        elif contributed_amount > required_amount:
            return "too much"
    return "sufficient"


def deduct_user_resources(user, contrib):
    """
    Deduct resources from the user based on the contribution.
    """
    for resource in user.resources:
        resource_type = resource.type.lower()
        if resource_type in contrib:
            resource.amount = max(resource.amount - contrib[resource_type], 0)
    db.session.add(user)
    db.session.commit()


def update_metrics(outcomes_str, user):
    """
    Update user and global metrics based on project outcomes.
    """
    outcomes = parse_resources(outcomes_str)
    for outcome_type, value in outcomes.items():
        # Update Common Metrics
        metric = CommonMetric.query.filter_by(type=outcome_type.capitalize()).first()
        if metric:
            metric.value += value
            db.session.add(metric)
    db.session.commit()
