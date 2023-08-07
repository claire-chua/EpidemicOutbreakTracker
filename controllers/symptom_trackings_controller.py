import functools
from flask import Blueprint, request
from psycopg2 import errorcodes
from init import db
from models.symptom_tracking import Symptom_Tracking, symptom_trackings_schema, symptom_tracking_schema
from models.user import User
from models.case import Case
from flask_jwt_extended import get_jwt_identity, jwt_required
from sqlalchemy import exc

symptom_trackings_bp = Blueprint('symptom_trackings', __name__, url_prefix='/symptom_trackings')
@symptom_trackings_bp.route('/', methods=['GET'])
def get_all_symptom_trackings():
    try:
        stmt = db.select(Symptom_Tracking)
        symptom_trackings = db.session.scalars(stmt)
        return symptom_trackings_schema.dump(symptom_trackings)
    except exc.SQLAlchemyError:
        return 'Table does not exist, please ensure to create all tables'
@symptom_trackings_bp.route('/<id>', methods=['GET'])
def get_one_symptom_tracking(id):
    stmt = db.select(Symptom_Tracking).filter_by(id=id)
    symptom_tracking = db.session.scalar(stmt)
    if symptom_tracking:
        return symptom_trackings_schema.dump(symptom_tracking)
    else:
        return {'error': f'Symptom Tracking id {id} not found'}, 404

@symptom_trackings_bp.route('/add', methods=['POST'])
@jwt_required()
def create_symptom_tracking():
    body_data = symptom_tracking_schema.load(request.get_json())
    symptom_tracking = Symptom_Tracking(
        id=body_data.get('id'),
        date=body_data.get('date'),
        symptoms=body_data.get('symptoms'),
        user_id=get_jwt_identity(),

    )
    db.session.add(symptom_tracking)
    db.session.commit()
    return symptom_tracking_schema.dump(symptom_tracking), 201
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

@symptom_trackings_bp.route('/<id>', methods=['DELETE'])
@jwt_required()
@authorise_as_admin
def delete_symptom_tracking(id):
    stmt = db.select(Case).filter_by(id=id)
    symptom_tracking = db.session.scalar(stmt)
    if symptom_tracking or str(symptom_tracking.user_id) == get_jwt_identity():
        db.session.delete(symptom_tracking)
        db.session.commit()
        return {'message': f'Symptom tracking id {id} deleted'}
    else:
        return {'error': f'Symptom tracking not found with id {id}'}, 404

@symptom_trackings_bp.route('/<int:id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_symptom_tracking(id):
    body_data = symptom_tracking_schema.load(request.get_json(), partial=True)
    stmt = db.select(Symptom_Tracking).filter_by(id=id)
    symptom_tracking = db.session.scalar(stmt)
    try:
        if symptom_tracking:
            if str(symptom_tracking.user_id) != get_jwt_identity():
                return {'error': 'Not authorised to edit case'}, 403
            symptom_tracking.id = body_data.get('id') or symptom_tracking.id
            symptom_tracking.date = body_data.get('date') or symptom_tracking.date
            symptom_tracking.symptoms = body_data.get('symptoms') or symptom_tracking.symptoms
            symptom_tracking.date = body_data.get('date') or symptom_tracking.date

            db.session.commit()
            return symptom_tracking_schema.dump(symptom_tracking)
        else:
            return {'error': f'Symptom tracking id {id} not found'}, 404
    except exc.IntegrityError as err:
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return {'Error': f'Unable to update case,{err.orig.diag.message_detail} '}, 409
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {'Error': f'The {err.orig.diag.column_name} is required'}, 409