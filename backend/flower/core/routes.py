from starlette.routing import Route, Mount
from starlette.staticfiles import StaticFiles

from .utils import make_response

from .permissions.resources import get_apps
from .users.resources import routes as user_routes
from .roles.resources import routes as roles_routes
from .sales.resources import routes as sales_routes
from .requests.resources import routes as request_routes
from .products.resources import routes as product_routes
from .branches.resources import routes as branches_routes
from .providers.resources import routes as provider_routes
from .contracts.resources import routes as contract_routes


async def ping(request):
    return make_response({'onPing': 'wePong'})

routes = [
    Mount('/media/', app=StaticFiles(directory='media'), name="media"),
    Route('/ping', ping),
    Route('/apps', get_apps, methods=['GET']),

    Mount('/users', routes=user_routes),
    Mount('/roles', routes=roles_routes),
    Mount('/sales', routes=sales_routes),
    Mount('/products', routes=product_routes),
    Mount('/requests', routes=request_routes),
    Mount('/branches', routes=branches_routes),
    Mount('/providers', routes=provider_routes),
    Mount('/contracts', routes=contract_routes),
]
