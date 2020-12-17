import pytest
from flower.config import ADMIN_USERNAME, ADMIN_PASSWORD

from tests.testconf import get_access_token, client, setup


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
