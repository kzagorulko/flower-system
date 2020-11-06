from starlette.routing import Route
from starlette.responses import JSONResponse
from ..utils import jwt_required
from ..models import RoleModel


@jwt_required(return_user=False)
async def get_roles(request):
    roles = await RoleModel.query.gino.all()
    return JSONResponse({
        'roles': [role.jsonify() for role in roles]
    })


routes = [
    Route('/', get_roles, methods=['GET'])
]
