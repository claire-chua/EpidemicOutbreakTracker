from flask import Blueprint
from init import db, bcrypt
from flask.cli import with_appcontext


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
    print("Tables dropped")
    return "success"
