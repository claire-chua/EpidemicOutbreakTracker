from flask import Blueprint
from init import db, bcrypt
from models.disease import Disease
from models.symptom_tracking import Symptom_Tracking
from models.user import User
from models.case import Case
from datetime import datetime

db_commands = Blueprint('db', __name__)


@db_commands.cli.command('create')
@db_commands.route('/create-tables')
def create_db():
    db.create_all()
    print("Tables Created")
    return "success"


@db_commands.cli.command('drop')
@db_commands.route('/drop-tables')
def drop_db():
    db.drop_all()
    print("Tables Dropped")
    return "success"


@db_commands.cli.command('seed')
@db_commands.route('/seed-tables')
def seed_db():
    users = [
        User(
            name='admin',
            email='admin@gmail.com',
            password=bcrypt.generate_password_hash('admincontrol').decode('utf-8'),
            id=1,
            is_admin=True,
        ),
        User(
            name='Claire',
            email='clair3.chua@gmail.com',
            password=bcrypt.generate_password_hash('clairecontrol').decode('utf-8'),
            id=2,
            is_admin=False,
        )

    ]
    db.session.add_all(users)

    cases = [
        Case(
            id=3,
            status='Active',
            date="15/08/2023",
            location='Australia,Melbourne',
            user_id=2,
            disease_id=2


        )
    ]
    db.session.add_all(cases)

    diseases = [
        Disease(
            id=1,
            name="Chickenpox",
            description="A contagious infection, which is characterised by an itchy, red which may develop into "
                        "fluid-filled blisters. Additional symptoms include; fever and headache. The symptoms "
                        "typically start two weeks after exposure and may be prevalent for 10 days to 3 weeks.",
            severity="Typically mild but can result in serious complications such as meningitis and pneumonia. Risk "
                     "Category: Pregnant woman, Newborn babies, Immunocompromised Individuals",
            vaccine="Yes",


        ),
        Disease(
            id=2,
            name="Ebola Virus",
            description="A rare but often fatal disease spread by fluids. ",
            severity="High",
            vaccine="Yes",


        )
    ]
    db.session.add_all(diseases)
    symptom_trackings = [
        Symptom_Tracking(
            id=1,
            date="2023/05/07",
            symptoms="fever,rash",
            user_id=1


        )
    ]
    db.session.add_all(symptom_trackings)
    db.session.commit()

    return 'Success'
    print('Tables Seeded')