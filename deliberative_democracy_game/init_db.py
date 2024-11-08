from app import create_app, db
from app.models import User, Project, CommonMetric, Resource, ProjectInsight
from app.utils import parse_resources

app = create_app()

with app.app_context():
    # Clear existing data to avoid duplicate entries
    db.session.query(ProjectInsight).delete()
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
    db.session.commit()

    # Add users (characters)
    users = [
        User(
            character_name="Maya – The Environmental Advocate",
            interests="Maya is an environmental scientist and activist who has been advocating for sustainable urban development for over a decade. Her goal is to ensure that every project incorporates eco-friendly practices that protect the environment and improve community health.",
            utility_criteria="Complete projects that yield positive Environment metrics and influence at least three projects to reduce their negative environmental impacts by half.",
            starting_resources="Labor: 10, Money: 10, Time: 10",
            reading="Research on environmental protection and urban sustainability.",
            environment=0,
            money=0,
            involvement=0,
            welfare=0,
        ),
        User(
            character_name="Tom – The Local Merchant",
            interests="Tom is a small business owner who operates a chain of eco-friendly stores. He sees the city’s development projects as potential to grow his business, support the local economy, and provide jobs for residents. However, he must carefully balance profitability with sustainability to maintain his customer base.",
            utility_criteria="Ensure projects benefit the local economy without overly sacrificing the environment. Invest in projects that yield positive economic returns.",
            starting_resources="Labor: 17, Money: 8, Time: 8",
            reading="Economic growth and business strategies.",
            environment=0,
            money=0,
            involvement=0,
            welfare=0,
        ),
        User(
            character_name="Nadia – The Single Mother and Community Organizer",
            interests="Nadia is a single mother with a deep commitment to improving quality of life in her community. She has organized local events, led initiatives for affordable housing, and works tirelessly to ensure her children have access to safe, healthy spaces in the city.",
            utility_criteria="Complete projects that provide accessible resources and welfare improvements for families. Ensure projects prioritize community welfare and safety.",
            starting_resources="Labor: 7, Money: 10, Time: 13",
            reading="Articles on family well-being and community support.",
            environment=0,
            money=0,
            involvement=0,
            welfare=0,
        ),
        User(
            character_name="Leo – The Builder and Infrastructure Expert",
            interests="Leo is a seasoned construction manager who sees each project as a challenge to improve the city’s infrastructure efficiently and sustainably. He is driven by a desire to create durable and functional structures that balance budget constraints with quality.",
            utility_criteria="Lead projects that improve urban infrastructure with minimal environmental impact. Use sustainable practices in projects.",
            starting_resources="Labor: 10, Money: 16, Time: 5",
            reading="Infrastructure projects and urban planning.",
            environment=0,
            money=0,
            involvement=0,
            welfare=0,
        ),
        User(
            character_name="Catharine – The Politician",
            interests="Catharine is a newly elected city council member committed to economic equity and environmental responsibility. She focuses on projects that achieve long-term benefits for the city, ensuring balanced growth for all residents.",
            utility_criteria="Support projects with balanced positive outcomes across Environment, Economy, and Welfare metrics.",
            starting_resources="Labor: 15, Money: 8, Time: 12",
            reading="Public service and policy-making articles.",
            environment=0,
            money=0,
            involvement=0,
            welfare=0,
        ),
    ]

    db.session.bulk_save_objects(users)
    db.session.commit()

    # Assign resources to each user based on their starting resources
    for user in users:
        user = User.query.filter_by(character_name=user.character_name).first()
        resources = parse_resources(user.starting_resources)

        for resource_type in ["Labor", "Money", "Time"]:
            amount = resources.get(resource_type.lower(), 0)
            resource = Resource(type=resource_type, amount=amount, user_id=user.id)
            db.session.add(resource)

    db.session.commit()

    # Add projects with personal metric updates
    projects = [
        Project(
            name="Grove Street Greenway",
            description="Transform vacant lots along Grove Street into community green spaces and gardens. "
            "<a href='https://docs.google.com/document/d/1EOCURNqVrgnFi-T7Rv0lNjLoCJWgeO8sP1NU2HkE5Y4/edit?usp=sharing' target='_blank'>Read more</a>",
            outcomes="Environment: +2, Economy: -1, Welfare: +1",
            required_resources="Labor: 4, Money: 2, Time: 3",
            personal_metric_updates={
                "1": {"Environment": 3, "Involvement": 1, "Welfare": 1},
                "2": {"Environment": 2, "Involvement": 1, "Welfare": 2},
                "3": {"Money": -1, "Involvement": 1, "Environment": 1},
                "4": {"Money": -1, "Involvement": 1, "Welfare": 1},
                "5": {"Money": 1, "Involvement": 1, "Welfare": 1},
            },
        ),
        Project(
            name="Riverside Tech Education Center",
            description="Establish a tech-focused educational center in Riverside."
            "<a href='https://docs.google.com/document/d/1EOCURNqVrgnFi-T7Rv0lNjLoCJWgeO8sP1NU2HkE5Y4/edit?usp=sharing' target='_blank'>Read more</a>",
            outcomes="Economy: +3, Welfare: +1",
            required_resources="Labor: 3, Money: 4, Time: 3",
            personal_metric_updates={
                "1": {"Environment": 1, "Involvement": 1},
                "2": {"Welfare": 2, "Involvement": 1},
                "3": {"Money": 2, "Involvement": 1},
                "4": {"Involvement": 1, "Welfare": 1},
                "5": {"Money": 1, "Involvement": 1},
            },
        ),
        Project(
            name="Horizon Electric Bus Fleet",
            description="Replace the aging city buses with electric buses in Horizon District."
            "<a href='https://docs.google.com/document/d/1EOCURNqVrgnFi-T7Rv0lNjLoCJWgeO8sP1NU2HkE5Y4/edit?usp=sharing' target='_blank'>Read more</a>",
            outcomes="Environment: +3, Welfare: +1",
            required_resources="Labor: 5, Money: 3, Time: 4",
            personal_metric_updates={
                "1": {"Environment": 3, "Involvement": 1},
                "2": {"Environment": 1, "Involvement": 1},
                "3": {"Money": 1, "Involvement": 1},
                "4": {"Welfare": 1, "Involvement": 1},
                "5": {"Money": 2, "Involvement": 1},
            },
        ),
        Project(
            name="Willow Park Affordable Housing",
            description="Develop affordable housing units in Willow Park."
            "<a href='https://docs.google.com/document/d/1EOCURNqVrgnFi-T7Rv0lNjLoCJWgeO8sP1NU2HkE5Y4/edit?usp=sharing' target='_blank'>Read more</a>",
            outcomes="Welfare: +2",
            required_resources="Labor: 3, Money: 4, Time: 2",
            personal_metric_updates={
                "1": {"Environment": 1, "Involvement": 1},
                "2": {"Welfare": 2, "Involvement": 1},
                "3": {"Money": 1, "Involvement": 1},
                "4": {"Involvement": 3},
                "5": {"Money": 1, "Involvement": 1},
            },
        ),
        Project(
            name="Solar Power Park at Sunnydale",
            description="Establish a solar power park at Sunnydale to transition the city to renewable energy."
            "<a href='https://docs.google.com/document/d/1EOCURNqVrgnFi-T7Rv0lNjLoCJWgeO8sP1NU2HkE5Y4/edit?usp=sharing' target='_blank'>Read more</a>",
            outcomes="Environment: +4, Economy: +2",
            required_resources="Labor: 4, Money: 5, Time: 4",
            personal_metric_updates={
                "1": {"Environment": 4, "Involvement": 1},
                "2": {"Welfare": 1, "Involvement": 1},
                "3": {"Money": 2, "Involvement": 1},
                "4": {"Environment": 1, "Involvement": 1},
                "5": {"Money": 2, "Involvement": 1},
            },
        ),
        Project(
            name="Meadowview Community Health Clinic",
            description="Build a subsidized healthcare center in Meadowview."
            "<a href='https://docs.google.com/document/d/1EOCURNqVrgnFi-T7Rv0lNjLoCJWgeO8sP1NU2HkE5Y4/edit?usp=sharing' target='_blank'>Read more</a>",
            outcomes="Welfare: +3",
            required_resources="Labor: 5, Money: 3, Time: 3",
            personal_metric_updates={
                "1": {"Involvement": 1},
                "2": {"Welfare": 3, "Involvement": 1},
                "3": {"Money": 1, "Involvement": 1},
                "4": {"Involvement": 2},
                "5": {"Money": 1, "Involvement": 1},
            },
        ),
        Project(
            name="Small Business Accelerator on Market Street",
            description="Launch a business accelerator on Market Street."
            "<a href='https://docs.google.com/document/d/1EOCURNqVrgnFi-T7Rv0lNjLoCJWgeO8sP1NU2HkE5Y4/edit?usp=sharing' target='_blank'>Read more</a>",
            outcomes="Economy: +3, Welfare: +1",
            required_resources="Labor: 3, Money: 4, Time: 2",
            personal_metric_updates={
                "1": {"Involvement": 1},
                "2": {"Welfare": 1, "Involvement": 1},
                "3": {"Money": 3, "Involvement": 2},
                "4": {"Involvement": 1},
                "5": {"Money": 1, "Involvement": 1},
            },
        ),
        Project(
            name="Valley Green Library Network",
            description="Establish a network of libraries in Valley Green."
            "<a href='https://docs.google.com/document/d/1EOCURNqVrgnFi-T7Rv0lNjLoCJWgeO8sP1NU2HkE5Y4/edit?usp=sharing' target='_blank'>Read more</a>",
            outcomes="Welfare: +2",
            required_resources="Labor: 4, Money: 2, Time: 3",
            personal_metric_updates={
                "1": {"Involvement": 1},
                "2": {"Welfare": 2, "Involvement": 1},
                "3": {"Money": 1, "Involvement": 1},
                "4": {"Involvement": 1},
                "5": {"Money": 1, "Involvement": 1},
            },
        ),
        Project(
            name="Coastal Wind Farm at Bayfront Shores",
            description="Install a wind farm along Bayfront Shores."
            "<a href='https://docs.google.com/document/d/1EOCURNqVrgnFi-T7Rv0lNjLoCJWgeO8sP1NU2HkE5Y4/edit?usp=sharing' target='_blank'>Read more</a>",
            outcomes="Environment: +5, Economy: -3",
            required_resources="Labor: 6, Money: 3, Time: 5",
            personal_metric_updates={
                "1": {"Environment": 5, "Involvement": 1},
                "2": {"Environment": 1, "Involvement": 1},
                "3": {"Money": 1, "Involvement": 1},
                "4": {"Involvement": 1},
                "5": {"Money": 1, "Involvement": 1},
            },
        ),
        Project(
            name="High-Tech Manufacturing Hub at Ironworks",
            description="Construct a high-tech manufacturing hub at the old Ironworks site."
            "<a href='https://docs.google.com/document/d/1EOCURNqVrgnFi-T7Rv0lNjLoCJWgeO8sP1NU2HkE5Y4/edit?usp=sharing' target='_blank'>Read more</a>",
            outcomes="Environment: -4, Economy: +5, Welfare: +1",
            required_resources="Labor: 5, Money: 6, Time: 4",
            personal_metric_updates={
                "1": {"Environment": -3, "Involvement": 1},
                "2": {"Money": 2, "Involvement": 1},
                "3": {"Money": 4, "Involvement": 2},
                "4": {"Involvement": 3, "Welfare": 1},
                "5": {"Money": 2, "Involvement": 1},
            },
        ),
    ]

    db.session.bulk_save_objects(projects)
    db.session.commit()

    print("Database initialized with users, resources, and detailed projects!")
