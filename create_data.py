import random
from random import choice, sample
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
from core.models import Base, Users, Competitions, Results, Whitelist

# Connect to the database
engine = create_engine('sqlite:///OSport.sqlite3')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# Clear the users table
session.query(Users).delete()
session.query(Competitions).delete()
session.query(Results).delete()
session.query(Whitelist).delete()

# Define sample data
sexes = ['М', 'Ж']
weights = [random.randint(50, 100) for _ in range(30)]
heights = [random.randint(150, 200) for _ in range(30)]
birth_dates = [datetime.now() - timedelta(days=random.randint(5000, 15000))
               for _ in range(30)]

# Create 30 unique users with all fields filled
for i in range(1, 31):
    user = Users(
        login=f'User{i}Login',
        email=f'User{i}@example.com',
        password=f'User{i}Password',
        first_name=f'User{i}',
        last_name=f'LastName{i}',
        birth_date=birth_dates[i-1],
        sex=choice(sexes),
        weight=weights[i-1],
        height=heights[i-1],
        total_experience=0.0,
        current_experience=0.0,
        created=datetime.now(),
        updated=datetime.now()
    )
    session.add(user)

# Commit users to the database
session.commit()

# Competition types
types = ['pushUps', 'squats', 'climber', 'bicycle', 'pullUps']

# Create 10 competitions
for i in range(1, 11):
    competition = Competitions(
        title=f'Competition{i}',
        type=choice(types),
        coefficient=round(random.uniform(0.5, 2.0), 2),
        video_instruction=f'VideoInstruction{i}',
        end_date=datetime.now() + timedelta(days=30),
        status=choice(['free', 'paid']),
        created=datetime.now(),
        updated=datetime.now()
    )
    session.add(competition)

# Commit competitions to the database
session.commit()

# Fetch all users and competitions
users = session.query(Users).all()
competitions = session.query(Competitions).all()

# Make each user participate in 6 random competitions
for user in users:
    user_competitions = sample(competitions, 6)
    for competition in user_competitions:
        count = random.randint(10, 100)
        coefficient = competition.coefficient
        points = count * coefficient
        status = choice(['checked_cv', 'wait_adm'])
        result = Results(
            competition_id=competition.competition_id,
            user_id=user.id,
            video=f'Video{user.id}_{competition.competition_id}',
            count=count,
            points=points,
            status=status,
            created=datetime.now(),
            updated=datetime.now()
        )
        session.add(result)

        # Update user's experience if status is 'checked_cv'
        if status == 'checked_cv':
            user.current_experience += 20 + points
            user.total_experience += 20 + points
            session.add(user)

        # If competition is paid, add user email to whitelist
        if competition.status == 'paid':
            whitelist_entry = Whitelist(
                competition_id=competition.competition_id,
                email=user.email,
                created=datetime.now(),
                updated=datetime.now()
            )
            session.add(whitelist_entry)

# Commit all results and whitelist entries to the database
session.commit()

print("Database populated successfully!")
