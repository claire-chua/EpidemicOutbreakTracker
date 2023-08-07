import functools

from flask import Blueprint, request
from psycopg2 import errorcodes

from init import db
from models.user import User
from models.case import Case, case_schema, cases_schema
from datetime import date
from flask_jwt_extended import get_jwt_identity, jwt_required
from sqlalchemy import exc

cases_bp = Blueprint('cases', __name__, url_prefix='/cases')


@cases_bp.route('/', methods=['GET'])
def get_all_cases():
    try:
        stmt = db.select(Case)
        cases = db.session.scalars(stmt)
        return cases_schema.dump(cases)
    except exc.SQLAlchemyError:
        return 'Table does not exist, please ensure to create all tables'

@cases_bp.route('/<id>')
def get_one_case(id):
    stmt = db.select(Case).filter_by(id=id)
    card = db.session.scalar(stmt)
    if card:
        return case_schema.dump(card)
    else:
        return {'error': f'Card id {id} not found'}, 404

@cases_bp.route('/add', methods=['POST'])
@jwt_required()
def create_case():
    body_data = case_schema.load(request.get_json())
    case = Case(
        id=body_data.get('id'),
        status=body_data.get('status'),
        date=body_data.get('date'),
        # user_id=body_data.get('user_id'),
        user_id=get_jwt_identity(),
        location=body_data.get('location'),
        disease_id=body_data.get('disease_id')
    )
    db.session.add(case)
    db.session.commit()
    return case_schema.dump(case), 201

def authorise_as_admin(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        case_id = get_jwt_identity()
        stmt = db.select(User).filter_by(id=case_id)
        user = db.session.scalar(stmt)
        if user.is_admin:
            return fn(*args, **kwargs)
        else:
            return {'error': 'Not authorised to perform delete'}, 403

    return wrapper

@cases_bp.route('/<id>', methods=['DELETE'])
@jwt_required()
@authorise_as_admin
def delete_case(id):
    stmt = db.select(Case).filter_by(id=id)
    case = db.session.scalar(stmt)
    if case or str(case.user_id) == get_jwt_identity() :
        db.session.delete(case)
        db.session.commit()
        return {'message': f'Case {id} deleted'}
    else:
        return {'error': f'Case not found with id {id}'}, 404

@cases_bp.route('/<int:id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_case(id):
    body_data = case_schema.load(request.get_json(), partial=True)
    stmt = db.select(Case).filter_by(id=id)
    case = db.session.scalar(stmt)
    try:
        if case:
            if str(case.user_id) != get_jwt_identity():
                return {'error': 'Not authorised to edit case'}, 403
            case.id = body_data.get('id') or case.id
            case.status = body_data.get('status') or case.status
            case.location = body_data.get('location') or case.location
            case.date = body_data.get('date') or case.date

            db.session.commit()
            return case_schema.dump(case)
        else:
            return {'error': f'Case id {id} not found'}, 404
    except exc.IntegrityError as err:
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return {'Error': f'Unable to update case,{err.orig.diag.message_detail} '}, 409
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {'Error': f'The {err.orig.diag.column_name} is required'}, 409