from init import db, ma
from marshmallow import fields, validates



class Symptom_Tracking(db.Model):
    __tablename__ = "symptom_trackings"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    symptoms = db.Column(db.String, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    users = db.relationship("User", back_populates='symptom_trackings', foreign_keys=[user_id])


class Symptom_TrackingSchema(ma.Schema):
    user = fields.List(fields.Nested('UserSchema', only=['name', 'email']))


    class Meta:
        fields = ('id', 'date', 'symptoms', 'user_id')


symptom_tracking_schema = Symptom_TrackingSchema()
symptom_trackings_schema = Symptom_TrackingSchema(many=True)
