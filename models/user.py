from init import db, ma
from marshmallow import fields



class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    phone_number = db.Column(db.Integer, unique=True)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    # case_id = db.Column(db.Integer, db.ForeignKey('case.id'), nullable=False)
    #
    cases = db.relationship('Case', back_populates='users',  cascade='all, delete')

class UserSchema(ma.Schema):
    case = fields.List(fields.Nested('CaseSchema', exclude=['user']))

    class Meta:
        fields = ('id', 'name','phone_number', 'email', 'password', 'is_admin')


user_schema = UserSchema(exclude=['password'])
users_schema = UserSchema(many=True, exclude=['password'])

