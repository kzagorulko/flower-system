from starlette.applications import Starlette

from .resources import routes


def create_app():
    from .models import db
    app = Starlette(
        debug=True,
        routes=routes
    )

    db.init_app(app)
    return app
