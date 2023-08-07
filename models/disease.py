from marshmallow import fields
from marshmallow.validate import OneOf

from init import db, ma

VALID_VACCINE_STATUSES = ('Yes', 'No', 'In Progress')

class Disease(db.Model):
    __tablename__ = 'diseases'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String, nullable=False, unique=True)
    severity = db.Column(db.String, nullable=False)
    vaccine = db.Column(db.String)


    # case_id = db.Column(db.Integer, db.ForeignKey('case.id'), nullable=False)
    #
    # cases = db.relationship('Cases', back_populates='diseases')

class DiseaseSchema(ma.Schema):
    case = fields.List(fields.Nested('DiseaseSchema', exclude=['user']))

    vaccine = fields.String(validate=OneOf(VALID_VACCINE_STATUSES))
    class Meta:
        fields = ('id', 'name', 'description', 'severity','vaccine','case_id')


disease_schema = DiseaseSchema()
diseases_schema = DiseaseSchema(many=True)

