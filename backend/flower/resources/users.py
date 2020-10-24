from starlette.routing import Route
from starlette.endpoints import HTTPEndpoint
from starlette.responses import JSONResponse, Response

from .utils import with_transaction
from ..models import UserModel, db


async def is_username_unique(username):
    user = await UserModel.query.where(
        UserModel.username == username
    ).gino.first()
    if user:
        return False
    return True


class Users(HTTPEndpoint):
    @staticmethod
    async def get(request):
        users_query = UserModel.query
        total_query = db.select([db.func.count(UserModel.id)])

        # TODO: add filters

        if 'pageSize' in request.query_params:
            page = int(request.query_params['page']) or 1
            page_size = int(request.query_params['pageSize'])
            users_query = users_query.limit(page_size).offset(page - 1)

        total = await total_query.gino.scalar()
        users = await users_query.gino.all()
        return JSONResponse({
            'items': [user.jsonify() for user in users],
            'total': total,
        })

    @with_transaction
    async def post(self, request):
        data = await request.json()
        if not await is_username_unique(data['username']):
            return JSONResponse({
                'description': f'User with username {data["username"]} is '
                f'already exist'
            }, status_code=400)
        new_user = await UserModel.create(username=data['username'])
        return JSONResponse({'id': new_user.id})


class User(HTTPEndpoint):
    @staticmethod
    async def get(request):
        user_id = request.path_params['user_id']
        user = await UserModel.get(user_id)
        if user:
            return JSONResponse(user.jsonify())
        return JSONResponse({
            'description': f'User with id {user_id} not found'
        }, status_code=404)

    @staticmethod
    @with_transaction
    async def patch(request):
        data = await request.json()
        user_id = request.path_params['user_id']
        user = await UserModel.get(user_id)
        if not user:
            return JSONResponse({
                'description': f'User with id {user_id} not found'
            }, status_code=404)
        if not await is_username_unique(data['username']):
            return JSONResponse({
                'description': f'User with username {data["username"]} is '
                f'already exist'
            }, status_code=400)
        # update username for example TODO: username should not be updated
        await user.update(username=data['username']).apply()

        return Response('', status_code=204)


routes = [
    Route('/', Users),
    Route('/{user_id:int}', User),
]
