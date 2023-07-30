from flask import Flask
import os
from init import db, ma, bcrypt, jwt


def create_app():
    app = Flask(__name__)

    # app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
    # app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2:claire_chua:12345@localhost:5432/EpidemicOutbreakTracker"
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://username:password@host:5432/database_name"

    # app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY")

    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    return app
