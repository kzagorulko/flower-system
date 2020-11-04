from ..database import db


class PermissionModel(db.Model):
    __tablename__ = 'permissions'

    id = db.Column(db.Integer, primary_key=True)
    app_name = db.Column(db.String(20), nullable=False)
    action = db.Column(db.String(20), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
