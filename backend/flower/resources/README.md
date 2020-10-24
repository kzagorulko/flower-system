# Ресурсы

Ссылка на коллекцию в постмане

[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/a38ca121a9a3f91c5675)

При работе с ресурсами пользуемся простыми правилами:

### Создание

Если создаёте ресурс для новой сущности, создайте отдельный файл, добавьте в
конец файла переменную `routes`, заполните её роутами, добивьте свой новый 
ресурс в `__init__`.

Пример:

Нужно сделать роуты для пользователей.

1. Создаём файл `users.py`
2. Создаём эндпойт:

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
```

3. Добавляем его в переменную `routes`:

```python
routes = [
    Route('/', Users),
]
```

обратите внимание на путь эндпойнта `'/'`. Префикс эндпойнта не нужно указывать
при роутинге в вашем ресурсе, он будет указан в дальнейшем.

4. Добавляем роуты юзера к общим роутам:

```python
from starlette.routing import Mount

from . import users

routes = [
    Mount('/users', routes=users.routes),
]
```

### Декораторы

Сейчас мы используем два декоратора: `@with_transaction` и `@staticmethod`.

Первый используется, когда что-то изменяется в базе данных. То есть во всех 
методах, кроме `get`. Второй используется в гет методах, если вам не нужно 
обращаться к классу через `self`. IDE обычно подствечивают метод, который можно
сделать статическим. 

### Запросы

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

### Ответы

При ответах придерживаемся следующих правил:

- При создании вернуть `id` новой сущности (`JSONResponse`)
- При обновлении данных, вернуть '', 204 NoContent (`Response`)
- При ошибке вернуть `{'description': '<Описание ошибки>'}` и обязательно
указать `status_code` (`JSONResponse`)

### Именование

Примеры:

путь: `/users/`

общий путь, через него обращаются к сущьности. 
именуем `Users`.

путь: `/users/{user_id:int}`
через него обращаются к конкретнуму пользователю.
именуем `User`.

