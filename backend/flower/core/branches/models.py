from ..database import db


class BranchModel(db.Model):
    __tablename__ = 'branches'

    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String, unique=True, nullable=False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._users = set()

    @property
    def users(self):
        return self._users

    @users.setter
    def users(self, value):
        self._users = value

    def jsonify(self, for_card=False):
        result = {
            'id': self.id,
            'address': self.address
        }

        if for_card:
            result['users'] = [
                user.jsonify() for user in self._users
            ]

        return result


class UserBranchModel(db.Model):
    __tablename__ = 'user_x_branch'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    branch_id = db.Column(
        db.Integer, db.ForeignKey('branches.id'), nullable=False
    )

    def jsonify(self):
        result = {
            'user_id': self.user_id,
            'branch_id': self.branch_id,
        }

        return result
