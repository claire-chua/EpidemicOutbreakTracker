import functools
import json
from datetime import timedelta

from flask import Blueprint, request, redirect, url_for, render_template
from flask_jwt_extended import verify_jwt_in_request, jwt_required, create_access_token, get_jwt_identity
from sqlalchemy import select

from init import db, bcrypt
from models.user import User, user_schema, users_schema
from sqlalchemy import exc
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes

users_bp = Blueprint('users', __name__, url_prefix='/users')


@users_bp.route('/all')
def get_all_users():
    try:
        stmt = db.select(User)
        users = db.session.scalars(stmt)
        return users_schema.dump(users)
    except exc.SQLAlchemyError:
        return 'Table does not exist, please ensure to create all tables'


@users_bp.route('/add', methods=['POST'])
def create_user():
    try:
        body_data = request.get_json()
        user = User()
        user.id = body_data.get('id')
        user.name = body_data.get('name')
        user.email = body_data.get('email')
        user.is_admin = body_data.get('is_admin')
        if body_data.get('password'):
            user.password = bcrypt.generate_password_hash(body_data.get('password')).decode('utf-8')

        db.session.add(user)
        db.session.commit()
        return user_schema.dump(user), 201
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return {'Error': f'Unable to create user,{err.orig.diag.message_detail} '}, 409
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {'Error': f'The {err.orig.diag.column_name} is required'}, 409


def authorise_as_admin(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()
        #filter by user_id to check for admin priviledge
        stmt = db.select(User).filter_by(id=user_id)
        user = db.session.scalar(stmt)
        if user.is_admin:
            return fn(*args, **kwargs)
        else:
            return {'error': 'Not authorised to perform delete'}, 403

    return wrapper


@users_bp.route('/<id>', methods=['DELETE'])
@jwt_required()
@authorise_as_admin
def delete_user(id):
    #filter by user id to delete user
    stmt = db.select(User).filter_by(id=id)
    user = db.session.scalar(stmt)
    if user:
        db.session.delete(user)
        db.session.commit()
        return {'message': f'User {id} has been deleted'}
    else:
        return {'error': f'User {id} not found'}, 404


@users_bp.route('/login', methods=['POST'])
def user_login():
    body_data = request.get_json()
    stmt = db.select(User).filter_by(email=body_data.get('email'))
    user = db.session.scalar(stmt)
    if user and bcrypt.check_password_hash(user.password, body_data.get('password')):
        token = create_access_token(identity=str(user.id), expires_delta=timedelta(days=0.5))
        return {'email': user.email, 'token': token, 'is_admin': user.is_admin}
    else:
        return {'error': 'Invalid email or password'}, 401


@users_bp.route('/<id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_user(id):
    body_data = user_schema.load(request.get_json(), partial=True)
    #filter by user id to update user details
    stmt = db.select(User).filter_by(id=id)
    user = db.session.scalar(stmt)
    try:
        if user:
            if str(id) != get_jwt_identity():
                return {'error': 'Not authorised to update login details'}, 403
            user.id = body_data.get('id') or user.id
            user.name = body_data.get('name') or user.name
            user.email = body_data.get('email') or user.email
            user.password = body_data.get('password') or user.password

            db.session.commit()
            return user_schema.dump(user)
        else:
            return {'error': f'User id {id} not found'}, 404
    except exc.IntegrityError as err:
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return {'Error': f'Unable to update user,{err.orig.diag.message_detail} '}, 409



