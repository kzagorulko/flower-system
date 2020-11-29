from enum import Enum
from ..database import db


class PurchaseStatus(Enum):
    NEW = 'NEW'
    IN_PROGRESS = 'IN_PROGRESS'
    CANCELLED = 'CANCELLED'
    DONE = 'DONE'

    def get_title(self):
        return {
            'NEW': 'Новая',
            'IN_PROGRESS': 'В работе',
            'CANCELLED': 'Отменена',
            'DONE': 'Завершена',
        }[self.name]


class PurchaseModel(db.Model):
    __tablename__ = 'purchases'

    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Float, nullable=False)
    status = db.Column(
        db.Enum(PurchaseStatus), nullable=False, default=PurchaseStatus.NEW
    )
    date = db.Column(db.DateTime(timezone=True), nullable=False)
    product_id = db.Column(
        db.Integer, db.ForeignKey('products.id'), nullable=True
    )
    warehouse_id = db.Column(
        db.Integer, db.ForeignKey('warehouses.id'), nullable=True
    )

    def jsonify(self):
        return {
            'id': self.id,
            'value': self.value,
            'status': self.status.get_title(),
            'product_id': self.product_id,
            'warehouse_id': self.warehouse_id
        }
