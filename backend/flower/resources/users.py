from starlette.routing import Route
from starlette.endpoints import HTTPEndpoint
from starlette.responses import JSONResponse, Response

from .utils import with_transaction

from ..core.user import *


class Users(HTTPEndpoint):
    @staticmethod
    async def get(request):
        user_repository = UserRepository()
        user_service = UserService(user_repository)

        users = await user_service.get_users(request.query_params)

        return JSONResponse({
            'items': [user.jsonify() for user in users],
            # 'total': total,
        })

    @with_transaction
    async def post(self, request):
        data = await request.json()

        try:
            user_repository = UserRepository()
            user_service = UserService(user_repository)
            user_id = await user_service.create_user(data['username'])

            return JSONResponse({'id': user_id})
        except UserAlreadyExistException as e:
            return JSONResponse({
                'description': e.args[0]
            }, status_code=400)


class User(HTTPEndpoint):
    @staticmethod
    async def get(request):
        user_id = request.path_params['user_id']
        try:
            user_repository = UserRepository()
            user_service = UserService(user_repository)
            user = await user_service.get_user_by_id(user_id)

            return JSONResponse(user.jsonify())
        except UserNotFoundException as e:
            return JSONResponse({
                'description': f'User with id {user_id} not found'
            }, status_code=404)

    @with_transaction
    async def patch(self, request):
        data = await request.json()
        user_id = request.path_params['user_id']

        try:
            user_repository = UserRepository()
            user_service = UserService(user_repository)
            await user_service.update_user(user_id, {
                'username': data['username']
            })

            return Response('', status_code=204)
        except (UserNotFoundException, UserAlreadyExistException) as e:
            return JSONResponse({
                'description': e[0].args[0]
            }, status_code=e[0].args[1])


routes = [
    Route('/', Users),
    Route('/{user_id:int}', User),
]
