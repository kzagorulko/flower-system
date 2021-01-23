from starlette.middleware import Middleware
from starlette.applications import Starlette
from starlette.middleware.cors import CORSMiddleware

middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_methods=['POST', 'GET', 'PATCH', 'DELETE', 'OPTIONS'],
        allow_headers=['*'])
]


def create_app():
    from . import db
    from .core import routes
    from .core.envents import startup_event
    from .config import TESTING

    app = Starlette(
        debug=True,
        routes=routes,
        middleware=middleware,
        on_startup=[startup_event]
    )
    if not TESTING:
        db.init_app(app)
    return app
