from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_methods=['POST', 'GET', 'PATCH', 'DELETE', 'OPTIONS'],
        allow_headers=['*'])
]


def create_app():
    from .core import db
    from .core import routes
    app = Starlette(
        debug=True,
        routes=routes,
        middleware=middleware
    )

    db.init_app(app)
    return app
