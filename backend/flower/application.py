import os

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
    from .config import TESTING

    app = Starlette(
        debug=True,
        routes=routes,
        middleware=middleware
    )
    if not TESTING:
        db.init_app(app)
    return app
