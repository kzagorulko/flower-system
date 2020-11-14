from ...config import SERVER_HOSTNAME
from ..database import db
from ..mediautils import MediaUtils


class ProductModel(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    price = db.Column(db.Float, nullable=False)
    image_path = db.Column(db.String(120), unique=True, nullable=False)
    description = db.Column(db.String(400), nullable=False)

    def jsonify(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'image_path': (SERVER_HOSTNAME
                           + MediaUtils.generate_full_path(self.image_path)),
            'description': self.description,
        }
