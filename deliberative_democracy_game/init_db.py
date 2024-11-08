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
            interests=(
                "Maya, a 42-year-old Latina environmental scientist and activist, "
                "grew up in a neighborhood affected by pollution and lack of green spaces. "
                "Inspired by her experiences, she pursued a career focused on sustainability and urban planning. "
                "Maya is deeply passionate about creating eco-friendly, livable urban areas and spends her free time "
                "teaching workshops on sustainable living practices. She has two teenage sons, aged 14 and 16, who often "
                "join her in community clean-up efforts and environmental awareness campaigns."
            ),
            utility_criteria="Achieve a total of 10 Environment metric points by the end of the game, and influence at least three projects to reduce their negative environmental impacts by 50%.",
            starting_resources="Labor: 10, Money: 10, Time: 10",
            reading="Research on environmental protection and urban sustainability.",
            environment=0,
            money=0,
            involvement=0,
            welfare=0,
        ),
        User(
            character_name="Tom – The Local Merchant",
            interests=(
                "Tom, a 38-year-old Asian-American entrepreneur, runs a chain of eco-friendly stores that sell sustainable "
                "household products. Growing up in a family that owned a small grocery store, Tom learned the importance of "
                "community engagement and supporting the local economy from an early age. He is driven by the desire to help "
                "local residents access sustainable goods at affordable prices. Tom is also an avid reader of economic growth "
                "strategies and enjoys volunteering at business mentorship programs."
            ),
            utility_criteria="Achieve at least 10 points in the Economy metric and 5 points in the Environment metric by the end of the game.",
            starting_resources="Labor: 17, Money: 8, Time: 8",
            reading="Economic growth and business strategies.",
            environment=0,
            money=0,
            involvement=0,
            welfare=0,
        ),
        User(
            character_name="Nadia – The Single Mother and Community Organizer",
            interests=(
                "Nadia, a 34-year-old African-American mother of three, has been dedicated to community activism since her "
                "early twenties. She grew up in a low-income household and vowed to improve living conditions for families in "
                "similar situations. Nadia's children, aged 4, 7, and 11, are her primary motivation for advocating for safer, "
                "more inclusive public spaces. In addition to her community work, she enjoys organizing family-friendly events "
                "and runs a support group for single parents. Her background includes leading neighborhood initiatives for "
                "affordable housing and fighting for better access to public resources."
            ),
            utility_criteria="Achieve at least 10 points in the Welfare metric and ensure at least two projects benefit families and community safety.",
            starting_resources="Labor: 7, Money: 10, Time: 13",
            reading="Articles on family well-being and community support.",
            environment=0,
            money=0,
            involvement=0,
            welfare=0,
        ),
        User(
            character_name="Leo – The Builder and Infrastructure Expert",
            interests=(
                "Leo, a 47-year-old Caucasian construction manager with over 20 years of experience, is known for his innovative "
                "and sustainable building practices. Raised in a family of engineers, he inherited a passion for constructing "
                "long-lasting infrastructure that stands the test of time. Leo has worked on numerous public projects that have "
                "improved urban transportation and housing. In his spare time, he enjoys designing model buildings and mentoring "
                "young architects. He firmly believes in balancing cost-effectiveness with quality to achieve the best results."
            ),
            utility_criteria="Achieve 10 points in Infrastructure-related Environment metrics and complete at least two major infrastructure projects with a net positive impact.",
            starting_resources="Labor: 10, Money: 16, Time: 5",
            reading="Infrastructure projects and urban planning.",
            environment=0,
            money=0,
            involvement=0,
            welfare=0,
        ),
        User(
            character_name="Catharine – The Politician",
            interests=(
                "Catharine, a 45-year-old African-American city council member, has a background in public administration and "
                "social work. She grew up watching her parents advocate for social justice and economic equity, which inspired her "
                "to pursue a career in politics. Catharine is a mother of one, a 10-year-old daughter who often joins her at public "
                "events and community gatherings. Her main goal is to implement policies that bridge the economic gap while preserving "
                "the city's natural resources. She enjoys reading about policy development and staying active in local cultural activities."
            ),
            utility_criteria="Ensure a balanced outcome of at least 5 points each in Environment, Economy, and Welfare metrics by the end of the game.",
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
            "<a href='https://docs.google.com/document/d/1GREZjA5OJdzQuPRxFNov1gTV-dGljg4jQiQscc0EDy8/edit?usp=sharing' target='_blank'>Read more</a>",
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
            "<a href='https://docs.google.com/document/d/19agfiSxbJ6jD_Xerclv21veMGeEMhl6WkAu-c4xEUMA/edit?usp=sharing' target='_blank'>Read more</a>",
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
            "<a href='https://docs.google.com/document/d/1JvL9652zRVkjtr52eggYR3MSm0_hnrmOoCyKscQ5b4U/edit?usp=sharing' target='_blank'>Read more</a>",
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
            "<a href='https://docs.google.com/document/d/1gOgPkwSLHkqyG3fHobbztA477zgbMqQIzUjsNFL69f0/edit?usp=sharing' target='_blank'>Read more</a>",
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
            "<a href='https://docs.google.com/document/d/11D4M_bQOLgZGVmoCbiQ7e5uSQ_shqov3kBgkNycg0Kk/edit?usp=sharing' target='_blank'>Read more</a>",
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
            "<a href='https://docs.google.com/document/d/13clxdj4hP6CqBGLsF_8vb2hRxwNi_ZNk-Tz3fe3yhFU/edit?usp=sharing' target='_blank'>Read more</a>",
            outcomes="Welfare: +3",
            required_resources="Labor: 2, Money: 3, Time: 3",
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
            "<a href='https://docs.google.com/document/d/1HpxaZLOoZSWTdYmYE2YitXBNZJSFqcVUWd0oq_qMkGI/edit?usp=sharing' target='_blank'>Read more</a>",
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
            "<a href='https://docs.google.com/document/d/12dHruLOsl-soPH_W5_OoDg_IaWD0yBr3nmIEauYDtW0/edit?usp=sharing' target='_blank'>Read more</a>",
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
            "<a href='https://docs.google.com/document/d/1j0Al90jXXjf0YVyxJjHNA6BBNXNzc43IeB5jF_gy1Dw/edit?usp=sharing' target='_blank'>Read more</a>",
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
            "<a href='https://docs.google.com/document/d/1G9SJvFquVHOuVvL24mDZJSGyGQikP8EMFkpaR25eV4A/edit?usp=sharing' target='_blank'>Read more</a>",
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
