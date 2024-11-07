from app import create_app, db
from app.models import User, Project, CommonMetric, Resource
from app.utils import parse_resources

app = create_app()

with app.app_context():
    # Clear existing data to avoid duplicate entries
    db.session.query(Resource).delete()
    db.session.query(User).delete()
    db.session.query(Project).delete()
    db.session.query(CommonMetric).delete()
    db.session.commit()

    db.create_all()

    # Initialize common metrics
    metrics = [
        CommonMetric(type="Environment", value=5),
        CommonMetric(type="Economy", value=5),
        CommonMetric(type="Welfare", value=5),
    ]
    db.session.bulk_save_objects(metrics)

    # Add users (characters)
    users = [
        User(
            character_name="Character 1",
            interests="Interest in environmental sustainability",
            utility_criteria="Achieve 10 Environment metric",
            starting_resources="Time: 3, Money: 2, Labor: 1",
            reading="Environmental impact studies and green initiatives.",
        ),
        User(
            character_name="Character 2",
            interests="Interest in economic growth",
            utility_criteria="Achieve 10 Economy metric",
            starting_resources="Time: 2, Money: 4, Labor: 1",
            reading="Economic strategies for city growth.",
        ),
        User(
            character_name="Character 3",
            interests="Interest in community welfare",
            utility_criteria="Achieve 10 Welfare metric",
            starting_resources="Time: 3, Money: 2, Labor: 2",
            reading="Social programs and community health.",
        ),
        User(
            character_name="Character 4",
            interests="Interest in balanced development",
            utility_criteria="Achieve a balanced score in all metrics",
            starting_resources="Time: 2, Money: 3, Labor: 2",
            reading="Integrated development plans.",
        ),
        User(
            character_name="Character 5",
            interests="Interest in rapid project execution",
            utility_criteria="Complete the most projects",
            starting_resources="Time: 4, Money: 1, Labor: 3",
            reading="Project management and efficiency strategies.",
        ),
    ]

    db.session.bulk_save_objects(users)
    db.session.commit()

    # Assign resources to each user based on their starting resources
    for user in users:
        user = User.query.filter_by(character_name=user.character_name).first()
        resources = parse_resources(user.starting_resources)
        for resource_type, amount in resources.items():
            resource = Resource(
                type=resource_type.capitalize(), amount=amount, user_id=user.id
            )
            db.session.add(resource)

    db.session.commit()

    # Add sample projects
    projects = [
        Project(
            name="Community Park Development",
            description="Develop a community park to improve green space in the neighborhood.",
            outcomes="Environment: +3, Welfare: +2",
            required_resources="Time: 4, Money: 2, Labor: 3",
        ),
        Project(
            name="Economic Growth Initiative",
            description="Upgrade local businesses to boost the economy and create jobs.",
            outcomes="Economy: +4, Environment: -1",
            required_resources="Time: 3, Money: 5",
        ),
        Project(
            name="Health Clinic Establishment",
            description="Build a new health clinic to enhance community healthcare.",
            outcomes="Welfare: +5, Economy: +2",
            required_resources="Time: 5, Labor: 4",
        ),
        Project(
            name="Renewable Energy Program",
            description="Initiate a renewable energy program to increase sustainability.",
            outcomes="Environment: +6, Economy: +3",
            required_resources="Time: 6, Money: 4",
        ),
        Project(
            name="Public Library Construction",
            description="Construct a public library to improve community education and welfare.",
            outcomes="Welfare: +3, Environment: +1",
            required_resources="Time: 4, Money: 3, Labor: 2",
        ),
    ]

    db.session.bulk_save_objects(projects)
    db.session.commit()

    print("Database initialized with users, resources, and projects!")
