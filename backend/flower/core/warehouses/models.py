from ..database import db


class WarehouseModel(db.Model):
    __tablename__ = 'warehouses'

    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(100), unique=True, nullable=False)
    max_value = db.Column(db.Float, nullable=False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._products = set()

    @property
    def products(self):
        return self._products

    @products.setter
    def products(self, value):
        self._products.add(value)

    def jsonify(self, for_card=False):
        result = {
            'id': self.id,
            'address': self.address,
            'max_value': self.max_value,
        }

        if for_card:
            result['products'] = [
                {
                    "product_id": product.product_id,
                    "value": product.value
                }
                for product in self.products
            ]

        return result


class ProductWarehouseModel(db.Model):
    __tablename__ = 'product_x_warehouse'

    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Float, nullable=False)
    product_id = db.Column(
        db.Integer, db.ForeignKey('products.id'), nullable=False
    )
    warehouse_id = db.Column(
        db.Integer, db.ForeignKey('warehouses.id'), nullable=False
    )

    def jsonify(self):
        result = {
            'product_id': self.product_id,
            'warehouse_id': self.warehouse_id,
        }

        return result
