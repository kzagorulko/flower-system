from starlette.routing import Route, Mount
from starlette.responses import JSONResponse

from .permissions.resources import get_apps
from .users.resources import routes as user_routes
from .roles.resources import routes as roles_routes
from .branches.resources import routes as branches_routes
from .providers.resources import routes as provider_routes
from .requests.resources import routes as request_routes


async def ping(request):
    return JSONResponse({'onPing': 'wePong'})

routes = [
    Route('/ping', ping),
    Route('/apps', get_apps, methods=['GET']),

    Mount('/users', routes=user_routes),
    Mount('/roles', routes=roles_routes),
    Mount('/requests', routes=request_routes),
    Mount('/branches', routes=branches_routes),
    Mount('/providers', routes=provider_routes),
]
