from ..database import db


class RequestCategoryModel(db.Model):
    __tablename__ = 'request_categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
