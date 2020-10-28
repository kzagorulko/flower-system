from gino_starlette import Gino
from .config import DB_HOST, DB_USER, DB_DATABASE, DB_PASSWORD, DB_PORT


db = Gino(
    driver='postgres',
    host=DB_HOST,
    port=DB_PORT,
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB_DATABASE
)


class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def jsonify(self):
        return {
            'id': self.id,
            'username': self.username,
        }

    @classmethod
    async def get_by_identifier(cls, identifier):
        return await cls.query.where(
            # (cls.email == identifier) | (cls.username == identifier)
            cls.username == identifier
        ).gino.first()
