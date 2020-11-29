from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import extract
from sqlalchemy import tuple_

from ..database import db


class SaleModel(db.Model):
    __tablename__ = 'sales'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._product = None
        self._branch = None

    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime(timezone=True), nullable=False)
    product_id = db.Column(
        db.Integer, db.ForeignKey('products.id'), nullable=True
    )
    branch_id = db.Column(
        db.Integer, db.ForeignKey('branches.id'), nullable=True
    )

    # гибридные свойства для даты
    @hybrid_property
    def date_month(self):
        return self.date.month

    @date_month.expression
    def date_month(self):
        return extract('month', self.date)

    @hybrid_property
    def date_year(self):
        return self.date.year

    @date_year.expression
    def date_year(self):
        return extract('year', self.date)

    @hybrid_property
    def date_month_year(self):
        return str(self.date_month) + "." + str(self.date_year)

    @date_month_year.expression
    def date_month_year(self):
        return tuple_(self.date_year, self.date_month)

    def jsonify(self):
        from ..utils import convert_to_utc
        return {
            'id': self.id,
            'value': self.value,
            'date': convert_to_utc(self.date).isoformat(),
            'product_id': self.product_id,
            'branch_id': self.branch_id,
        }
