from starlette.routing import Route, Mount
from starlette.responses import JSONResponse

from .database import db

from . import users


async def ping(request):
    return JSONResponse({'onPing': 'wePong'})

routes = [
    Route('/ping', ping),
    Mount('/users', routes=users.routes),
]

__all__ = [
    'routes',
    'db',
]
