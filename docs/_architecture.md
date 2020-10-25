# Архитектура системы

## Архитектура в общем

Используется `MVC`:
- V - визуализация на стороне `frontend`
- C - ресурсы на стороне `backend`
- M - бизнес-логина на стороне `backend`

## Backend

В свою очередь `M` в текущей системе MVC - большая часть, которая реализуется
в соответствии с многослойной архитектурой `Domain-driven design` (паттерны `Entity`, `Repository`, `Service` и др.)

### Тесты

Юнит тестирования слоя сервисов, где реализуется основная бзнес-логика.
Используется `Dependency Injection` для изоляции логики от фреймворков.

#### Пример

(/tests/test_user_service.py)

#### Код для создания пользователя

```python

user_repository = UserRepository()
user_service = UserService(user_repository)
await user_service.create_user('test_name')
```

#### Конструктор UserService

В это время конструктор `UserService` принимает объект класса (интерфейс)
`UserRepositoryPort`, что позволяет подставлять туда любые нужные нам объекты.

Так как всё взаимодействие с фреймворком происходит в `UserRepository`, который наследуется
от `UserRepositoryPort`, для тестирования можно заменить репозиторий
на нужный нам объект и протестировать бизнес-логику

```python
def get_fake_repository(unique_name=True):
    class UserRepositoryFake:
        async def create_user(self, username):
            return UserEntity(id=1, username=username)

        async def is_username_unique(self, username):
            return unique_name

    return UserRepositoryFake()

user_rep = get_fake_repository(unique_name=False)
user_service = UserService(user_rep)
```


