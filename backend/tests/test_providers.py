from tests.testconf import get_access_token, client, setup


def test_provider_create(client):
    access_token = get_access_token(client)
    response = client.post(
        '/providers/',
        headers={'Authorization': f'Bearer {access_token}'},
        json={
            'name': 'Израильская роза',
            'data': 'Новый поставщик роз на рынке.',
            'email': 'test@mail.com',
            'address': 'Пушкина, 1',
        }
    )

    assert response.status_code == 200, response.text
    data = response.json()
    assert 'id' in data


def test_provider_update(client):
    access_token = get_access_token(client)
    response = client.patch(
        '/providers/3',
        headers={'Authorization': f'Bearer {access_token}'},
        json={
            'phone': '+79997779922',
        }
    )

    assert response.status_code == 204, response.text
