from marshmallow import fields

from init import db, ma


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)


    cases = db.relationship('Case', back_populates='users',  cascade='all, delete')
    symptom_trackings=db.relationship('Symptom_Tracking', back_populates='users')
class UserSchema(ma.Schema):
    case = fields.List(fields.Nested('CaseSchema', exclude=['user']))
    symptom_tracking = fields.List(fields.Nested('Symptom_TrackingSchema', exclude=['user']))
    class Meta:
        fields = ('id', 'name', 'email', 'password', 'is_admin')


user_schema = UserSchema(exclude=['password'])
users_schema = UserSchema(many=True, exclude=['password'])

