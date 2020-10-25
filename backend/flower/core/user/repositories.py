"""
Репозитории
- для работы с фреймворками и сторонними инетрсументами
"""

from zope.interface import implementer
from .dbModels import UserModel
from .mappers import UserMapper
from .entities import UserEntity
from .ports import UserRepositoryPort
from .exceptions import UserNotFoundException, UserAlreadyExistException

@implementer(UserRepositoryPort)
class UserRepository:
    def __init__(self):
        pass

    async def get_by_id(self, id: int) -> UserEntity:
        user = await UserModel.get(id)
        if not user:
            raise UserNotFoundException

        return UserMapper.map_user_entity_from_user_model(user)

    async def create_user(self, username) -> UserEntity:
        return UserMapper.map_user_entity_from_user_model(
            await UserModel.create(username=username)
        )

    async def update_user(self, user_id, data) -> UserEntity:
        user = await UserModel.get(user_id)

        if not user:
            raise UserNotFoundException(f'User with id {user_id} not found', 404)

        if not self.is_username_unique(data['username']):
            raise UserAlreadyExistException(f'User with username {data["username"]} is '
                f'already exist', 400)

        # update username for example TODO: username should not be updated
        await user.update(username=data['username']).apply()

        return UserMapper.map_user_entity_from_user_model(user)

    async def is_username_unique(self, username) -> bool:
        user = await UserModel.query.where(
            UserModel.username == username
        ).gino.first()
        if user:
            return False
        return True

    async def get_users(self, filter: list) -> list:
        users_query = UserModel.query
        #total_query = db.select([db.func.count(UserModel.id)])

        # TODO: add filters

        if 'pageSize' in filter:
            page = int(filter['page']) or 1
            page_size = int(filter['pageSize'])
            users_query = users_query.limit(page_size).offset(page - 1)

        #total = await total_query.gino.scalar()
        users = await users_query.gino.all()

        return [UserMapper.map_user_entity_from_user_model(user) for user in users]

