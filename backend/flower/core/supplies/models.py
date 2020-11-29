from ..database import db


class SupplyModel(db.Model):
    __tablename__ = 'supplies'

    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime(timezone=True), nullable=False)
    product_id = db.Column(
        db.Integer, db.ForeignKey('products.id'), nullable=True
    )
    warehouse_id = db.Column(
        db.Integer, db.ForeignKey('warehouses.id'), nullable=True
    )
    branch_id = db.Column(
        db.Integer, db.ForeignKey('branches.id'), nullable=True
    )

    def jsonify(self):
        return {
            'id': self.id,
            'value': self.value,
            'product_id': self.product_id,
            'warehouse_id': self.warehouse_id,
            'branch_id': self.branch_id,
        }
