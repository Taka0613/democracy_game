import unittest
from app import create_app, db
from app.models import User, Project, ProjectInsight
from flask_login import login_user
from flask import url_for


class TestInsightFeature(unittest.TestCase):
    def setUp(self):
        """Set up a test app and test database."""
        self.app = create_app()
        self.app.config["TESTING"] = True
        self.app.config["SQLALCHEMY_DATABASE_URI"] = (
            "sqlite:///:memory:"  # In-memory database
        )
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

            # Create a test user and project
            user = User(
                character_name="testuser",
                interests="Interest in testing",
                utility_criteria="Complete test cases",
                starting_resources="Labor: 2, Money: 2, Time: 2",
                reading="Testing methodologies and practices.",
            )
            project = Project(name="Test Project", description="A test project")

            db.session.add(user)
            db.session.add(project)
            db.session.commit()

            # Create a test insight
            insight = ProjectInsight(
                user_id=user.id,
                project_id=project.id,
                insight="This is a test insight.",
            )
            db.session.add(insight)
            db.session.commit()

            self.user_id = user.id  # Store user_id for testing

    def tearDown(self):
        """Tear down the test database."""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_insight_display(self):
        """Test if insights are displayed correctly on the 'My Insights' page."""
        with self.app.test_request_context():
            with self.client as client:
                # Simulate user login
                user = User.query.get(self.user_id)
                login_user(user)

                # Access the "My Insights" page
                response = client.get(url_for("main.insight"))

                # Check if the response contains the test insight
                self.assertEqual(response.status_code, 200)
                self.assertIn(b"This is a test insight.", response.data)
                self.assertIn(b"Test Project", response.data)


if __name__ == "__main__":
    unittest.main()
