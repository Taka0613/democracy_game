# app/models.py

from . import db
from flask_login import UserMixin


# User Model
class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    character_name = db.Column(db.String(64), unique=True, nullable=False)
    interests = db.Column(db.Text, nullable=True)
    utility_criteria = db.Column(db.Text, nullable=True)
    starting_resources = db.Column(db.Text, nullable=True)
    reading = db.Column(db.Text, nullable=True)

    # Relationships
    resources = db.relationship("Resource", backref="user", lazy=True)
    metrics = db.relationship("Metric", backref="user", lazy=True)

    def __repr__(self):
        return f"<User {self.character_name}>"


# Resource Model
class Resource(db.Model):
    __tablename__ = "resources"

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(64), nullable=False)  # 'Time', 'Money', 'Labor'
    amount = db.Column(db.Integer, default=0, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    def __repr__(self):
        return (
            f"<Resource {self.type} (Amount: {self.amount}) for User ID {self.user_id}>"
        )


# Project Model
class Project(db.Model):
    __tablename__ = "projects"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text, nullable=True)
    outcomes = db.Column(db.Text, nullable=True)
    required_resources = db.Column(db.Text, nullable=True)
    is_completed = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<Project {self.name}>"


# Metric Model
class Metric(db.Model):
    __tablename__ = "metrics"

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(
        db.String(64), nullable=False
    )  # 'Environment', 'Economy', 'Welfare'
    value = db.Column(db.Integer, default=0, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)


# Common Metric Model
class CommonMetric(db.Model):
    __tablename__ = "common_metrics"

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(
        db.String(64), nullable=False
    )  # 'Environment', 'Economy', 'Welfare'
    value = db.Column(db.Integer, default=0, nullable=False)


# Completed Project Model
class CompletedProject(db.Model):
    __tablename__ = "completed_projects"

    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey("projects.id"), nullable=False)
    completed_by_user_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False
    )
    completion_date = db.Column(db.DateTime, nullable=False)
