from enum import Enum
from ..database import db


class PurchaseStatus(Enum):
    NEW = 'NEW'
    IN_PROGRESS = 'IN_PROGRESS'
    CANCELLED = 'CANCELLED'
    DONE = 'DONE'


class PurchaseModel(db.Model):
    __tablename__ = 'purchases'

    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Float, nullable=False)
    address = db.Column(db.String(100), unique=True, nullable=False)
    status = db.Column(
        db.Enum(PurchaseStatus), nullable=False, default=PurchaseStatus.NEW
    )
    date = db.Column(db.DateTime(timezone=True), nullable=False)
    product_id = db.Column(
        db.Integer, db.ForeignKey('products.id'), nullable=False
    )
    warehouse_id = db.Column(
        db.Integer, db.ForeignKey('warehouses.id'), nullable=False
    )
    contract_id = db.Column(
        db.Integer, db.ForeignKey('warehouses.id'), nullable=False
    )

    def jsonify(self):
        from ..utils import convert_to_utc
        return {
            'id': self.id,
            'value': self.value,
            'address': self.address,
            'status': self.status.name,
            'product_id': self.product_id,
            'warehouse_id': self.warehouse_id,
            'date': convert_to_utc(self.date).isoformat(),
        }
