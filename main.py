import os

from controllers.cli_controller import db_commands
from flask import Flask

from controllers.cli_controller import db_commands
from controllers.diseases_controller import diseases_bp
from controllers.symptom_trackings_controller import symptom_trackings_bp
from controllers.users_controller import users_bp
from controllers.cases_controller import cases_bp
from init import db, ma, bcrypt, jwt
from controllers.cases_controller import cases_bp


def create_app():
    app = Flask(__name__)

    # app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://postgres:1234@localhost:5432/epidemic_tracker"
    #app.config["JWT_SECRET_KEY"] = (os.environ.get("JWT_SECRET_KEY"))
    app.config["JWT_SECRET_KEY"] = 'secret'


    @app.errorhandler(400)
    def bad_request(err):
        return {'error': str(err)}, 400

    @app.errorhandler(404)
    def not_found(err):
        return {'error': str(err)}, 404

    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    app.register_blueprint(db_commands)
    app.register_blueprint(users_bp)
    app.register_blueprint(cases_bp)
    app.register_blueprint(diseases_bp)
    app.register_blueprint(symptom_trackings_bp)

    return app
