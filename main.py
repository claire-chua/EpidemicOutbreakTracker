import os

from controllers.cli_controller import db_commands
from flask import Flask

from controllers.cli_controller import db_commands
from controllers.users_controller import users_bp
from controllers.cases_controller import cases_bp
from init import db, ma, bcrypt, jwt
from controllers.cases_controller import cases_bp


def create_app():
    app = Flask(__name__)

    # app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
    # app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2:claire_chua:12345@localhost:5432/EpidemicOutbreakTracker"
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://postgres:1234@localhost:5432/epidemic_tracker"

    app.config["JWT_SECRET_KEY"] = "secret"
    # (os.environ.get("JWT_SECRET_KEY"))

    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    app.register_blueprint(db_commands)
    app.register_blueprint(users_bp)
    app.register_blueprint(cases_bp)

    return app
