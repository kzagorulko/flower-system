from starlette.routing import Route, Mount
from starlette.responses import JSONResponse

from .users.resources import routes as user_routes
from .roles.resources import routes as roles_routes


async def ping(request):
    return JSONResponse({'onPing': 'wePong'})

routes = [
    Route('/ping', ping),
    Mount('/users', routes=user_routes),
    Mount('/roles', routes=roles_routes),
]
