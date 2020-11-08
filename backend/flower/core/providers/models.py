from enum import Enum
from ..database import db


class ProviderStatusTypes(Enum):
    NEW = 0
    COOPERATE = 1
    FRAUD = 2
    STOPPED = 3


class ProviderModel(db.Model):
    __tablename__ = 'providers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(50))
    phone = db.Column(db.String(12))
    status = db.Column(db.Enum(ProviderStatusTypes), nullable=False)
    data = db.Column(db.String(400), nullable=False)
    address = db.Column(db.String(100), nullable=False)

    def jsonify(self, for_card=False):
        result = {
            'id': self.id,
            'name': self.name,
            'status': self.status.name.lower(),
        }
        if for_card:
            result['email'] = self.email
            result['phone'] = self.phone
            result['data'] = self.data
            result['address'] = self.address
        return result
