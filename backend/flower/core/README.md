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

Если создаёте часть ядра для новой сущности, создайте отдельный пакет, 
в пакет могут входить файлы `models.py`, `resources.py`, `utils` и
обязательно входит файл `__init__.py`. 

- После создания модели, она сначала
добавляется в `<название пакета>/__init__.py`, а затем в `core/models.py`.
Импортировать модели также стоит использовать из `core.models.py`. 

- После создания ресурса нужо добавить в конец файла переменную `routes`, 
заполните её роутами. Затем следует добавить ресурс в `__init__`.

Пример:

Нужно сделать роуты для пользователей.

1. Создаём пакет `users`.
2. Создаём модель `UserModel`:

```python
from ... import db


class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
```

3. Добавляем модель в `users/__init__.py`:

```python
from .models import UserModel

__all__ = ['UserModel']

```

4. Добавляем модель в `core/models.py`:

```python
from .users import UserModel

__all__ = ['UserModel']

```

5. Создаём эндпойт или функцию:

```python
from starlette.endpoints import HTTPEndpoint
from starlette.responses import JSONResponse

from ..models import UserModel


class User(HTTPEndpoint):
    @staticmethod
    async def get(request):
        user_id = request.path_params['user_id']
        user = await UserModel.get(user_id)
        if user:
            return JSONResponse(user.jsonify())
            
async def ping(request):
    return JSONResponse({'onPing': 'wePong'})
```


6. Добавляем его в переменную `routes`:

```python
routes = [
    Route('/', Users),
    Route('/', ping, methods=['GET'])
]
```

обратите внимание на путь эндпойнта `'/'`. Префикс эндпойнта не нужно указывать
при роутинге в вашем ресурсе, он будет указан в дальнейшем.

7. Добавляем роуты к нешей моделе в `users/__init__.py`:

```python
from .models import UserModel
from .resources import routes

__all__ = ['routes', 'UserModel']

```

8. Добавляем роуты юзера к общим роутам:

```python
from starlette.routing import Route, Mount

from . import users

routes = [
    Mount('/users', routes=users.routes),
]

__all__ = ['routes']
```

### <a name="Wrappers"></a> Декораторы

Сейчас мы используем три декоратора: `@with_transaction`, `@staticmethod` 
`jwt_required`.

Первый используется, когда что-то изменяется в базе данных. То есть во всех 
методах, кроме `get`. Второй используется в гет методах, если вам не нужно 
обращаться к классу через `self`. IDE обычно подствечивают метод, который можно
сделать статическим. 

`jwt_required` имеет опциональный интрефейс. Можно писать просто 

```python
@jwt_required
async def get_blank_response(request):
    return Response('', status_code=204)
```

или

```python
@jwt_required(reutrn_user=True)
async def get_user_username(request, user):
    return Response(user.username)
```

также в этом декораторе имеется опциональный параметр `token_type`, но
его вряд ли придётся использовать.

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

- При создании вернуть `id` новой сущности (`JSONResponse`)
- При обновлении данных, вернуть '', 204 NoContent (`Response`)
- При ошибке вызвать функцию `utils/make_error`, передать <Описание ошибки>
и указать `status_code` (`JSONResponse`)

### <a name="Naming"></a> Именование

Примеры:

путь: `/users/`

общий путь, через него обращаются к сущьности. 
именуем `Users`.

путь: `/users/{user_id:int}`
через него обращаются к конкретнуму пользователю.
именуем `User`.

