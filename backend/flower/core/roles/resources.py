from starlette.routing import Route

from ..utils import jwt_required, make_response
from ..models import RoleModel


@jwt_required(return_user=False)
async def get_roles(request):
    roles = await RoleModel.query.gino.all()
    return make_response({
        'roles': [role.jsonify() for role in roles]
    })


routes = [
    Route('/', get_roles, methods=['GET'])
]
