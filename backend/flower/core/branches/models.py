from ..database import db


class BranchModel(db.Model):
    __tablename__ = 'branches'

    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String, unique=True, nullable=False)

    def jsonify(self):
        result = {
            'id': self.id,
            'address': self.address
        }

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
