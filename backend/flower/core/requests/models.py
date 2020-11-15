from enum import Enum
from ..database import db


class RequestStatus(Enum):
    NEW = 0
    IN_PROGRESS = 1
    CANCELLED = 2
    DONE = 3

    def get_title(self):
        return {
            'NEW': 'Новая',
            'IN_PROGRESS': 'В работе',
            'CANCELLED': 'Отменена',
            'DONE': 'Завершена',
        }[self.name]


class RequestModel(db.Model):
    __tablename__ = 'requests'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(400), nullable=False, default='')
    created = db.Column(db.DateTime(timezone=True), nullable=False)
    status = db.Column(db.Enum(RequestStatus), nullable=False, default='NEW')

    creator_id = db.Column(
        db.Integer, db.ForeignKey('users.id'), nullable=False
    )
    departament_id = db.Column(
        db.Integer, db.ForeignKey('roles.id'), nullable=False
    )
    category_id = db.Column(
        db.Integer, db.ForeignKey('request_categories.id'), nullable=False
    )
    executor_id = db.Column(
        db.Integer, db.ForeignKey('users.id'), nullable=True
    )

    def __init__(self,  **kwargs):
        super().__init__(**kwargs)
        self._departament = None
        self._creator = None
        self._category = None
        self._executor = None

    @property
    def departament(self):
        return self._departament

    @departament.setter
    def departament(self, value):
        self._departament = value

    @property
    def creator(self):
        return self._creator

    @creator.setter
    def creator(self, value):
        self._creator = value

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        self._category = value

    @property
    def executor(self):
        return self._executor

    @executor.setter
    def executor(self, value):
        self._executor = value

    def jsonify(self, for_card=False):
        print(self.id, self.departament_id, self.departament)
        result = {
            'id': self.id,
            'name': self.name,
            'departament': self.departament.display_name,
            'status': self.status.get_title(),
            'created': self.created.strftime('%d.%m.%Y %H:%M')
        }

        if for_card:
            result['description'] = self.description
            result['category'] = self.category.name
            result['creator'] = self.creator.jsonify()
            result['executor'] = self.executor and self.executor.jsonify()

        return result


class RequestCategoryModel(db.Model):
    __tablename__ = 'request_categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    def jsonify(self):
        return {
            'id': self.id,
            'name': self.name,
        }

