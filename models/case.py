from init import db, ma
from marshmallow import fields, validates
from marshmallow.validate import OneOf
from models.user import User



VALID_STATUSES = ('Active', 'Suspected')


class Case(db.Model):
    __tablename__ = "cases"

    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String)
    location = db.Column(db.String, nullable=False)
    date = db.Column(db.Date)
    #
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    # disease_id = db.Column(db.String, db.ForeignKey('diseases.id'))

    users = db.relationship("User", back_populates='cases', foreign_keys=[user_id])


    # disease = db.relationship('Disease', back_populates='cases')


class CaseSchema(ma.Schema):
    user = fields.List(fields.Nested('UserSchema', only=['name', 'email']))
    # disease = fields.List(fields.Nested('DiseaseSchema'), only=['name'])

    status = fields.String(validate=OneOf(VALID_STATUSES))

    class Meta:
        fields = ('id', 'status', 'location', 'date', 'user_id')


case_schema = CaseSchema()
cases_schema = CaseSchema(many=True)
