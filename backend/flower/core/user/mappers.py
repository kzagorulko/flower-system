"""
Для преобразования dbModel в Entity
"""

from .entities import UserEntity
from .dbModels import UserModel

class UserMapper:
    @staticmethod
    def map_user_entity_from_user_model(user: UserModel) -> UserEntity:
        return UserEntity(
            id=user.id,
            username=user.username
        )