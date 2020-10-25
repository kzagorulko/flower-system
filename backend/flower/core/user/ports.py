"""
Интерфейсы
"""

import zope.interface
from .entities import UserEntity


class UserRepositoryPort(zope.interface.Interface):
    async def get_by_id(self, id: int) -> UserEntity:
        """Get UserEntity By Id"""

    async def get_users(self, filter: dict) -> list:
        """Get users with filtration"""

    async def create_user(self, username) -> UserEntity:
        """Create user by with username"""

    async def update_user(self, user_id, data) -> UserEntity:
        """Update user by id, data -> dict"""

    async def is_username_unique(self, username) -> bool:
        """"""


class UserServicePort(zope.interface.Interface):
    async def get_user_by_id(self, id: int) -> dict:
        """"""

    async def get_users(self, filter: dict) -> list:
        """"""

    async def create_user(self, username: str) -> int:
        """"""

    async def update_user(self, user_id, data) -> UserEntity:
        """"""
