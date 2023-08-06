# from marshmallow import fields
# from init import db, ma
#
#
# class Disease(db.Model):
#     __tablename__ = 'diseases'
#
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String)
#     description = db.Column(db.String, nullable=False, unique=True)
#     severity = db.Column(db.String, nullable=False)
#
#
#     # case_id = db.Column(db.Integer, db.ForeignKey('case.id'), nullable=False)
#     #
#     cases = db.relationship('Case', back_populates='users',  cascade='all, delete')
#
# class DiseaseSchema(ma.Schema):
#     case = fields.List(fields.Nested('DiseaseSchema', exclude=['user']))
#
#     class Meta:
#         fields = ('id', 'name', 'description', 'severity')
#
#
# disease_schema = DiseaseSchema()
# diseases_schema = DiseaseSchema(many=True)
#
