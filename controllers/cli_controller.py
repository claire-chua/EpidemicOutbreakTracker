from flask import Blueprint
from init import db, bcrypt
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
            phone_number='0413294923',
            password=bcrypt.generate_password_hash('admincontrol').decode('utf-8'),
            id=1,
            is_admin=True,
        ),
        User(
            name='Claire',
            email='clair3.chua@gmail.com',
            phone_number='0449179562',
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
            date=datetime.now(),
            location='Australia,Melbourne',
            user_id=2,

        )
    ]
    db.session.add_all(cases)
    db.session.commit()

    return 'Success'
    print('Tables Seeded')