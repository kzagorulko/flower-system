import nest_asyncio
nest_asyncio.apply()

import pytest
from starlette.testclient import TestClient
from alembic.config import Config
from alembic import command


from flower.config import DB_URL, ADMIN_USERNAME, ADMIN_PASSWORD
from flower.application import create_app
from flower.core.database import db


@pytest.fixture(autouse=True)
async def setup():
    """
    Create a clean test database every time the tests are run.
    """
    print(DB_URL)
    async with db.with_bind(DB_URL):
        alembic_config = Config('./alembic.ini')
        command.upgrade(alembic_config, 'head')
        yield                            # Run the tests.
        # await db.gino.drop_all()         # Drop the test database.


def get_client():
    """
    Make a 'client' fixture available to test cases.
    """
    # Our fixture is created within a context manager. This ensures that
    # application startup and shutdown run for every test case.
    #
    # Because we've configured the DatabaseMiddleware with
    # `rollback_on_shutdown` we'll get a complete rollback to the initial state
    # after each test case runs.
    app = create_app()
    with TestClient(app) as test_client:
        return test_client


client = get_client()


def get_access_token():
    response = client.post(
        '/users/refresh-tokens', json={
            'identifier': ADMIN_USERNAME,
            'password': ADMIN_PASSWORD
        }
    )
    return response.json()['access_token']


def test_ping():
    response = client.get('/ping')

    assert response.status_code == 200, response.text


def test_tokens():
    response = client.post(
        '/users/refresh-tokens', json={
            'identifier': ADMIN_USERNAME,
            'password': ADMIN_PASSWORD
        }
    )

    assert response.status_code == 200, response.text


def test_get_obj():
    access_token = get_access_token()
    response = client.get(
        '/users',
        headers={'Authorization':  f'Bearer {access_token}'}
    )
    assert response.status_code == 200, response.text
    data = response.json()
    # assert data['name'] == my_object.name

