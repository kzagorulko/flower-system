from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

from .resources import routes

middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_methods=['POST', 'GET', 'PATCH', 'DELETE'],
        allow_headers=['content-type'])
]


def create_app():
    from .models import db
    app = Starlette(
        debug=True,
        routes=routes,
        middleware=middleware
    )

    db.init_app(app)
    return app
