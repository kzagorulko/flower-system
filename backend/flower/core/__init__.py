from starlette.routing import Route, Mount
from starlette.responses import JSONResponse

from .database import db
from .users import UserModel
from .roles import RoleModel

from . import users


async def ping(request):
    return JSONResponse({'onPing': 'wePong'})

routes = [
    Route('/ping', ping),
    Mount('/users', routes=users.routes),
]

__all__ = [
    'routes',
    'UserModel',
    'RoleModel',
    'db',
]
