from enum import Enum
from datetime import date
from ..database import db
from ...config import SERVER_HOSTNAME


class ContractStatus(Enum):
    NOT_STARTED = 0
    OPERATING = 1
    CANCELLED = 2
    DONE = 3

    @classmethod
    def get_by_date(cls, start_date, end_date):
        if date.today() < start_date:
            return cls.NOT_STARTED
        elif date.today() > end_date:
            return cls.DONE
        return cls.OPERATING


class ContractModel(db.Model):
    __tablename__ = 'contracts'

    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(40), nullable=False)
    status = db.Column(
        db.Enum(ContractStatus),
        nullable=False,
        default=ContractStatus.NOT_STARTED
    )
    path = db.Column(db.String(120), nullable=False)
    start_date = db.Column(db.DateTime(timezone=True), nullable=False)
    end_date = db.Column(db.DateTime(timezone=True), nullable=False)
    provider_id = db.Column(
        db.Integer, db.ForeignKey('providers.id'), nullable=False
    )
    cancel_description = db.Column(db.String(400), nullable=False, default='')

    def jsonify(self, for_card=False):
        from ..utils import MediaUtils, convert_to_utc
        result = {
            'id': self.id,
            'number': self.number,
            'status': self.status.name,
            'startDate': convert_to_utc(self.start_date).isoformat(),
            'endDate': convert_to_utc(self.end_date).isoformat(),
        }

        if for_card:
            result['providerId'] = self.provider_id
            result['path'] = (
                SERVER_HOSTNAME + MediaUtils.generate_full_path(self.path)
            )
            if self.cancel_description:
                result['cancelDescription'] = self.cancel_description

        return result
