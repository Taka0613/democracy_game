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


# utils.py


def calculate_total_score(environment_score, economy_score, welfare_score):
    """
    Calculate the total score based on the individual scores for environment, economy, and welfare.
    The function considers both the sum of scores and the balance between them.

    Parameters:
    - environment_score (int): The score for the environment.
    - economy_score (int): The score for the economy.
    - welfare_score (int): The score for welfare.

    Returns:
    - int: The calculated total score as a percentage (0 to 100).
    """
    # Calculate the total sum of the scores
    total_sum = environment_score + economy_score + welfare_score

    # Find the balance by calculating the standard deviation (lower is better)
    scores = [environment_score, economy_score, welfare_score]
    mean_score = total_sum / 3
    balance_penalty = sum((score - mean_score) ** 2 for score in scores) / 3

    # Adjust the balance penalty to a percentage range (higher balance gives higher score)
    balance_score = max(0, 100 - balance_penalty)

    # Combine the total sum and balance to create a comprehensive score
    total_score = (total_sum / 3) * 0.7 + balance_score * 0.3  # Weighted combination

    # Ensure the total score is capped between 0 and 100
    return min(100, max(0, int(total_score)))


def calculate_personal_metric_updates(project, user):
    """Calculate and update the personal metrics for a user based on the project outcomes."""
    if not hasattr(project, "personal_metric_updates"):
        return  # No metric updates defined for this project

    # Update user's personal metrics based on the project's personal_metric_updates
    for metric, value in project.personal_metric_updates.items():
        if metric == "Environment":
            user.environment = (user.environment or 0) + value
        elif metric == "Money":
            user.money = (user.money or 0) + value
        elif metric == "Involvement":
            user.involvement = (user.involvement or 0) + value
        elif metric == "Welfare":
            user.welfare = (user.welfare or 0) + value
