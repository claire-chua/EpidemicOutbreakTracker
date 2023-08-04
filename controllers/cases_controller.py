from flask import Blueprint, request
from init import db
from models.user import User
from models.case import Case, case_schema, cases_schema
from datetime import date
from flask_jwt_extended import get_jwt_identity, jwt_required

cases_bp = Blueprint('cases', __name__, url_prefix='/cases')


@cases_bp.route('/', methods=['GET'])

def get_all_cases():
    try:

        stmt = db.select(Case)
        cases = db.session.scalars(stmt)
        return cases_schema.dump(cases)
    except:
        return 'Error, no cards to retrieve'


@cases_bp.route('/add', methods=['POST'])
# @jwt_required()
def create_case():
    body_data = case_schema.load(request.get_json())
    # create a new Card model instance
    case = Case(
        id=body_data.get('id'),
        status=body_data.get('status'),
        date=date.today(),
        user_id=body_data.get('user_id'),
        # get_jwt_identity(),
        location=body_data.get('location')
    )
    db.session.add(case)
    db.session.commit()
    return case_schema.dump(case), 201
