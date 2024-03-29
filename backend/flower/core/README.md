# Ядро

Ссылка на коллекцию в постмане

[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/a38ca121a9a3f91c5675)

При работе с частями ядра пользуемся правилами:

- [Создание](#Create)
- [Декораторы](#Wrappers)
- [Запросы](#Requests)
- [Ответы](#Responses)
- [Именование](#Naming)

### <a name="Create"></a> Создание

Если создаёте часть ядра для новой сущности, создайте отдельную папку, 
в папку могут входить файлы `models.py`, `resources.py`, `utils`. 

- После создания модели, она добавляется `core/models.py`.
Импортировать модели также стоит из `core.models.py`. 

- После создания ресурса нужно добавить в конец файла переменную `routes`, 
заполните её роутами. Затем следует добавить ресурс в `core/routes.py`.

Пример:

Нужно сделать роуты для пользователей.

1. Создаём папку `users`.
2. Создаём модель `UserModel`:

```python
from ..database import db


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
```

3. Добавляем модель в `core/models.py`:

```python
from .users.models import UserModel

__all__ = ['UserModel']

```

4. Создаём эндпойт или функцию:

```python
from starlette.endpoints import HTTPEndpoint

from ..models import UserModel
from ..utils import make_error, make_response


class User(HTTPEndpoint):
    @staticmethod
    async def get(request):
        user_id = request.path_params['user_id']
        user = await UserModel.get(user_id)
        if user:
            return make_response(user.jsonify())
        return make_error(description='User not found', status_code=404)
            
async def ping(request):
    return make_response({'onPing': 'wePong'})
```


5. Добавляем его в переменную `routes`:

```python
routes = [
    Route('/', User),
    Route('/ping', ping, methods=['GET'])
]
```

обратите внимание на путь эндпойнта `'/'`. Префикс эндпойнта не нужно указывать
при роутинге в вашем ресурсе, он будет указан в дальнейшем.

6. Добавляем роуты юзера к общим роутам:

```python
from starlette.routing import Mount

from .users.resources import routes as users_routes

routes = [
    Mount('/users', routes=users_routes),
]

__all__ = ['routes']
```

### <a name="Wrappers"></a> Декораторы

Сейчас мы используем декораторы: `@with_transaction`, `@staticmethod`, 
`jwt_required`, `permissions.required`.

#### with_transaction

Используется, когда что-то изменяется в базе данных. То есть во всех 
методах, кроме `get`. 

**НЕ используется вместе с `@staticmethod`**

#### staticmethod

Используется в гет методах, если вам не нужно обращаться к классу через 
`self`. IDE обычно подствечивают метод, который можно сделать статическим. 

#### jwt_required

`jwt_required` имеет опциональный интрефейс. Можно писать просто 

```python
@jwt_required(return_user=False)
async def get_blank_response(request):
    return Response('', status_code=204)
```

или

```python
@jwt_required
async def get_user_username(request, user):
    return Response(user.username)
```

как видно, `return_user` стоит по умолчанию в значении `True`. И если вам
он не нужен, то можете убрать его, передпав атрибут `return_user` со
значением `False`. Также в этом декораторе имеется опциональный параметр 
`token_type`, но его вряд ли придётся использовать.

#### Permissions

В отличие от прошлых декораторов, этот является не функцией, а классом
поэтому его следует объявлять заранее с указанием имени приложения,
в котором он будет работать:

```python
from ..utils import Permissions

permissions = Permissions(app_name='users')
```

Использовать его следует, когда ваш метод должен быть ограничен полномочиями.
```python
@with_transaction
@jwt_required
@permissions.required(action='delete')
async def delete_all_users(request):
    await Users.delete.gino.status()
    return Response('', status_code=204)

```

также у него есть аргументы: `return_user` и `return_role`, которые по 
умолчанию установлены в `False`


### <a name="Requests"></a> Запросы

- `json` тело:
```python
data = await request.json()
```

- параметры из пути (`/users/1`) (получить 1)
```python
user_id = request.path_params['user_id']
```

- параметр запроса (`/users/1?role=admin) (роль юзера)
```python
role = request.query_params['role']
```

### <a name="Responses"></a>Ответы

При ответах придерживаемся следующих правил:

- При создании вернуть `id` новой сущности `make_response(content)`  
из `core/utils`
- При возврате сущности также вернуть `make_response(content)`
- При возврате списка вернуть `make_list_response(<items>, <total>)`
 из `core/utils`
- При обновлении данных, вернуть константу `NO_CONTENT` из `core/utils`
- При ошибке вызвать функцию `make_error` из `core/utils`, передать описание
ошибки и указать `status_code`

### <a name="Naming"></a> Именование

Примеры:

путь: `/users/`

общий путь, через него обращаются к сущьности. 
именуем `Users`.

путь: `/users/{user_id:int}`
через него обращаются к конкретнуму пользователю.
именуем `User`.

