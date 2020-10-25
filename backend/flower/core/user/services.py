from zope.interface import implementer
from .ports import UserServicePort, UserRepositoryPort
from .exceptions import UserAlreadyExistException
from .entities import UserEntity


@implementer(UserServicePort)
class UserService:
    def __init__(self, user_repository: UserRepositoryPort):
        self.user_repository = user_repository

    async def get_user_by_id(self, id: int) -> UserEntity:
        return await self.user_repository.get_by_id(id)

    async def get_users(self, filter: dict) -> list:
        return await self.user_repository.get_users(filter)

    async def create_user(self, username: str) -> int:
        if not await self.user_repository.is_username_unique(username):
            raise UserAlreadyExistException(f'User with username {username} is already exist', 400)

        return (await self.user_repository.create_user(username)).id

    async def update_user(self, user_id, data) -> UserEntity:
        return await self.user_repository.update_user(user_id, data)
