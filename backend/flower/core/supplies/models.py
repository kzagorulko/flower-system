from enum import Enum
from ..database import db


class SupplyStatus(Enum):
    NEW = 'NEW'
    IN_PROGRESS = 'IN_PROGRESS'
    CANCELLED = 'CANCELLED'
    DONE = 'DONE'


class SupplyModel(db.Model):
    __tablename__ = 'supplies'

    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Float, nullable=False)
    status = db.Column(
        db.Enum(SupplyStatus), nullable=False, default=SupplyStatus.NEW
    )
    date = db.Column(db.DateTime(timezone=True), nullable=False)
    product_id = db.Column(
        db.Integer, db.ForeignKey('products.id'), nullable=False
    )
    warehouse_id = db.Column(
        db.Integer, db.ForeignKey('warehouses.id'), nullable=False
    )
    branch_id = db.Column(
        db.Integer, db.ForeignKey('branches.id'), nullable=False
    )

    def jsonify(self):
        from ..utils import convert_to_utc
        return {
            'id': self.id,
            'value': self.value,
            'product_id': self.product_id,
            'warehouse_id': self.warehouse_id,
            'branch_id': self.branch_id,
            'status': self.status.name,
            'date': convert_to_utc(self.date).isoformat(),
        }
