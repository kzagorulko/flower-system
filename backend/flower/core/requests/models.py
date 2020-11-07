from ..database import db


class RequestModel(db.Model):
    __tablename__ = 'requests'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(400), nullable=False, default='')
    created = db.Column(db.DateTime(timezone=True), nullable=False)

    creator_id = db.Column(
        db.Integer, db.ForeignKey('users.id'), nullable=False
    )
    departament_id = db.Column(
        db.Integer, db.ForeignKey('roles.id'), nullable=False
    )
    category_id = db.Column(
        db.Integer, db.ForeignKey('request_categories.id'), nullable=False
    )
