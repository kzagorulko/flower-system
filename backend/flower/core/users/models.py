from .. import db


class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    # TODO change default to False
    activated = db.Column(db.Boolean, nullable=False, default=True)
    display_name = db.Column(db.String(50), nullable=False)
    path_to_image = db.Column(db.String(120))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=True)

    def jsonify(self, for_card=False):
        result = {
            'id': self.id,
            'displayName': self.display_name,

        }

        if for_card:
            result['username'] = self.username
            result['email'] = self.email
            result['activated'] = self.activated

        result['role'] = ''

        return result

    @classmethod
    async def get_by_identifier(cls, identifier):
        return await cls.query.where(
            (cls.email == identifier) | (cls.username == identifier)
        ).gino.first()

    @classmethod
    def get_column_for_order(cls, column_name, asc=True):
        names_x_columns = {
            'id': cls.id,
            'displayName': cls.display_name,
        }

        if asc:
            return names_x_columns[column_name]
        return names_x_columns[column_name].desc()

