# app/routes.py
from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    request,
    flash,
    current_app,
)
from flask_login import login_user, login_required, logout_user, current_user
from .models import db, User, Project, CommonMetric, Resource, ProjectInsight
from .forms import LoginForm, ProjectInsightForm
from .utils import parse_resources, deduct_user_resources, update_metrics
from . import login_manager  # Only import the necessary initialized extensions

# Create Blueprint
main = Blueprint("main", __name__, template_folder="templates")


@login_manager.user_loader
def load_user(user_id):
    """Load a user by ID for Flask-Login."""
    return User.query.get(int(user_id))


# Login Route
@main.route("/", methods=["GET", "POST"])
def login():
    """Handle the login of users."""
    form = LoginForm()
    if form.validate_on_submit():
        character_name = form.character_name.data
        user = User.query.filter_by(character_name=character_name).first()
        if user:
            login_user(user)
            flash("Logged in successfully.", "success")
            return redirect(url_for("main.dashboard"))
        else:
            flash("Character not found.", "danger")
    return render_template("login.html", form=form)


# Dashboard Route
@main.route("/dashboard")
@login_required
def dashboard():
    """Display the user dashboard."""
    user = User.query.get(current_user.id)
    return render_template("dashboard.html", user=user)


# Project List Route
@main.route("/projects")
@login_required
def project_list():
    """List all active projects available for contribution."""
    projects = Project.query.filter_by(is_completed=False).all()
    return render_template("project_list.html", projects=projects)


# Project Detail Route
@main.route("/project/<int:project_id>", methods=["GET", "POST"])
@login_required
def project_detail(project_id):
    """Display project details and handle user contributions."""
    project = Project.query.get_or_404(project_id)
    users = User.query.all()
    required_resources = parse_resources(project.required_resources)
    user_insights = {}

    if request.method == "POST":
        # Collect contributions and insights from form inputs
        contributions = collect_contributions(users, request)
        user_insights = {
            user.id: request.form.get(f"policy_insight_{user.id}", "") for user in users
        }

        # Validate user contributions
        if not validate_contributions(users, contributions):
            flash("Contributions are not valid. Check resource availability.", "danger")
            return render_template(
                "project_detail.html",
                project=project,
                users=users,
                user_insights=user_insights,
            )

        # Sum total contributions and check project completion
        if not check_project_completion(contributions, required_resources):
            return render_template(
                "project_detail.html",
                project=project,
                users=users,
                user_insights=user_insights,
            )

        # Complete the project if validations pass
        complete_project(project, contributions)
        flash("Project completed successfully!", "success")
        return redirect(url_for("main.finished_projects"))

    return render_template(
        "project_detail.html", project=project, users=users, user_insights=user_insights
    )


@main.route("/finished_projects")
@login_required
def finished_projects():
    """Display a list of completed projects."""
    projects = Project.query.filter_by(is_completed=True).all()
    total_projects = Project.query.count()  # Get the total number of projects
    return render_template(
        "finished_projects.html", projects=projects, total_projects=total_projects
    )


# Scoreboard Route
@main.route("/scoreboard")
@login_required
def score_board():
    """Display the scoreboard showing common metrics."""
    common_metrics = CommonMetric.query.all()
    return render_template("score_board.html", metrics=common_metrics)


# Logout Route
@main.route("/logout")
@login_required
def logout():
    """Log out the current user."""
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("main.login"))


# Helper Functions
def collect_contributions(users, request):
    """Collect contributions from form inputs."""
    contributions = {}
    for user in users:
        contributions[user.id] = {
            "time": int(request.form.get(f"contribute_time_{user.id}", 0)),
            "money": int(request.form.get(f"contribute_money_{user.id}", 0)),
            "labor": int(request.form.get(f"contribute_labor_{user.id}", 0)),
        }
    return contributions


def validate_contributions(users, contributions):
    """Validate that contributions do not exceed user resources."""
    for user in users:
        user_contrib = contributions[user.id]
        for resource in user.resources:
            resource_type = resource.type.lower()
            contribution_amount = user_contrib.get(resource_type, 0)
            if contribution_amount > resource.amount:
                flash(
                    f"{user.character_name}'s contribution exceeds available {resource.type}.",
                    "danger",
                )
                return False
    return True


def check_project_completion(contributions, required_resources):
    """Check if total contributions meet project requirements."""
    total_contributed = {
        "labor": sum(contrib["labor"] for contrib in contributions.values()),
        "money": sum(contrib["money"] for contrib in contributions.values()),
        "time": sum(contrib["time"] for contrib in contributions.values()),
    }
    if any(
        total_contributed[res] > required_resources.get(res, 0)
        for res in required_resources
    ):
        flash("Contributions exceed the required resources.", "danger")
        return False
    elif any(
        total_contributed[res] < required_resources.get(res, 0)
        for res in required_resources
    ):
        flash(
            "Contributions are not enough to meet the project requirements.", "warning"
        )
        return False
    return True


def complete_project(project, contributions):
    """Complete the project by deducting user resources and updating metrics."""
    for user_id, contrib in contributions.items():
        user = User.query.get(user_id)
        if user:
            deduct_user_resources(user, contrib)
    update_metrics(project.outcomes, current_user)
    project.is_completed = True
    db.session.commit()


# app/routes.py


@main.route("/insight")
@login_required
def insight():
    """Display insights written by the current user."""
    insights = ProjectInsight.query.filter_by(user_id=current_user.id).all()
    return render_template("insight.html", insights=insights)
