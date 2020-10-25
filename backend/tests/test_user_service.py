import pytest

from backend.flower.core.user import *


def get_fake_repository(unique_name=True):
    class UserRepositoryFake:
        async def create_user(self, username):
            return UserEntity(id=1, username=username)

        async def is_username_unique(self, username):
            return unique_name

    return UserRepositoryFake()


@pytest.mark.asyncio
# @pytest.mark.xfail(raises=UserAlreadyExistException)
async def test_create_not_unique_user():  # pylint: disable=redefined-outer-name
    user_rep = get_fake_repository(unique_name=False)

    user_service = UserService(user_rep)

    try:
        await user_service.create_user('ivan')
        assert False
    except UserAlreadyExistException:
        assert True


@pytest.mark.asyncio
async def test_create_user_success():
    user_rep = get_fake_repository()

    user_service = UserService(user_rep)
    user_id = await user_service.create_user('ivan')

    assert user_id == 1
