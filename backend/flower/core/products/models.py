from ..database import db


class ProductModel(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    price = db.Column(db.Float, nullable=False)
    image_path = db.Column(db.String(120), unique=True, nullable=False)
    description = db.Column(db.String(400), nullable=False)

    def jsonify(self):
        from ..utils import MediaUtils
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'image_path': MediaUtils.get_url(self.image_path),
            'description': self.description,
        }
