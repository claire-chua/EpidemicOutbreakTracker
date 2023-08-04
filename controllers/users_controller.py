import json
from datetime import timedelta

from flask import Blueprint, request
from flask_jwt_extended import verify_jwt_in_request, jwt_required, create_access_token
from sqlalchemy import select

from init import db, bcrypt
from models.user import User, user_schema

users_bp = Blueprint('users', __name__, url_prefix='/users')


@users_bp.route('/all')
def get_all_users():
    getUsers = select(User)
    results = db.session.scalars(getUsers).first()

    # db.create_all()
    # getUsers = db.select(User)
    # users = db.session.scalars(getUsers)

    return user_schema.dump(results)


@users_bp.route('/add', methods=['POST'])
def create_user():
    # try:
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


# except:
#     return 'Error'
@users_bp.route('/login', methods=['POST'])
def user_login():
    body_data = request.get_json()
    # Find the user by email address
    stmt = db.select(User).filter_by(email=body_data.get('email'))
    user = db.session.scalar(stmt)
    # If user exists and password is correct
    if user and bcrypt.check_password_hash(user.password, body_data.get('password')):
        token = create_access_token(identity=str(user.id), expires_delta=timedelta(days=1))
        return ('Success')
    else:
        return {'error': 'Invalid email or password'}, 401
