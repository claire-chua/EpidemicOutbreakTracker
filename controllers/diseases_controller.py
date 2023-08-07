import sqlalchemy.exc
from sqlalchemy.exc import IntegrityError

from models import disease
from models.disease import Disease, diseases_schema, disease_schema
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

@diseases_bp.route('/<id>', methods=['GET'])
def get_one_disease_type(id):
    stmt = db.select(Disease).filter_by(id=id)
    disease = db.session.scalar(stmt)
    if disease:
        return disease_schema.dump(disease)
    else:
        return {'error': f'Disease id {id} not found'}, 404

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
@diseases_bp.route('/<id>', methods=['DELETE'])
@jwt_required()
@authorise_as_admin
def delete_case(id):
    stmt = db.select(Disease).filter_by(id=id)
    disease = db.session.scalar(stmt)
    if disease:
        db.session.delete(disease)
        db.session.commit()
        return {'message': f'Disease {id} deleted'}
    else:
        return {'error': f'Disease id {id} not found'}, 404

@diseases_bp.route('/<id>', methods=['PUT', 'PATCH'])
@jwt_required()
@authorise_as_admin
def update_case(id):
    body_data = case_schema.load(request.get_json(), partial=True)
    stmt = db.select(Disease).filter_by(id=id)
    disease = db.session.scalar(stmt)
    try:
        if disease:
            disease.id = body_data.get('id') or disease.id
            disease.status = body_data.get('status') or disease.status
            disease.location = body_data.get('location') or disease.location
            disease.date = body_data.get('date') or disease.date

            db.session.commit()
            return case_schema.dump(disease)
        else:
            return {'error': f'Disease id {id} not found'}, 404
    except exc.IntegrityError as err:
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return {'Error': f'Unable to update,{err.orig.diag.message_detail} '}, 409
@diseases_bp.route('/add', methods=['POST'])
@jwt_required()
def create_disease_type():
    try:
        body_data = disease_schema.load(request.get_json())
        disease = Disease(
            id=body_data.get('id'),
            description=body_data.get('description'),
            name=body_data.get('name'),
            # user_id=body_data.get('user_id'),
            severity=body_data.get('severity'),
            vaccine=body_data.get('vaccine')
        )
    except exc.IntegrityError as err:
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return {'Error': f'Unable to create disease type,{err.orig.diag.message_detail} '}, 409
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {'Error': f'The {err.orig.diag.column_name} is required'}, 409
    db.session.add(disease)
    db.session.commit()
    return disease_schema.dump(disease), 201