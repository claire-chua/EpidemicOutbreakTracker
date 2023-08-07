from models.disease import Disease, diseases_schema
import functools

from flask import Blueprint, request
from psycopg2 import errorcodes

from init import db
from models.user import User
from models.case import Case, case_schema, cases_schema
from datetime import date
from flask_jwt_extended import get_jwt_identity, jwt_required
from sqlalchemy import exc

diseases_bp = Blueprint('diseases', __name__, url_prefix='/diseases')


@diseases_bp.route('/all', methods=['GET'])
def get_all_disease_types():
    try:
        stmt = db.select(Disease)
        diseases = db.session.scalars(stmt)
        return diseases_schema.dump(diseases)
    except exc.SQLAlchemyError:
        return 'Table does not exist, please ensure to create all tables'