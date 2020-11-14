from starlette.routing import Route, Mount
from starlette.responses import JSONResponse
from starlette.staticfiles import StaticFiles

from .users.resources import routes as user_routes
from .roles.resources import routes as roles_routes
from .permissions.resources import get_apps
from .providers.resources import routes as provider_routes
from .branches.resources import routes as branch_routes
from .products.resources import routes as product_routes
from .sales.resources import routes as sales_routes


async def ping(request):
    return JSONResponse({'onPing': 'wePong'})

routes = [
    Mount('/media/', app=StaticFiles(directory='media'), name="media"),
    Route('/ping', ping),
    Route('/apps', get_apps, methods=['GET']),
    Mount('/users', routes=user_routes),
    Mount('/roles', routes=roles_routes),
    Mount('/branches', routes=branch_routes),
    Mount('/providers', routes=provider_routes),
    Mount('/products', routes=product_routes),
    Mount('/sales', routes=sales_routes),
]
