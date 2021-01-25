from uuid import uuid4

from starlette.routing import Route
from starlette.endpoints import HTTPEndpoint
from passlib.hash import pbkdf2_sha256 as sha256

from ..database import db
from ..models import UserModel, RoleModel, BranchModel
from ..utils import (
    with_transaction, create_refresh_token, create_access_token, jwt_required,
    make_error, Permissions, GinoQueryHelper, make_list_response,
    make_response, NO_CONTENT,
)

from .utils import (
    is_username_unique, get_role_id, RoleNotExist
)

permissions = Permissions(app_name='users')


class Users(HTTPEndpoint):
    @staticmethod
    @jwt_required
    @permissions.required(action=permissions.actions.GET)
    async def get(request):
        users_query = UserModel.outerjoin(RoleModel).select()
        total_query = db.select(
                            [db.func.count(UserModel.id)]
                    ).select_from(UserModel.outerjoin(RoleModel))

        query_params = request.query_params

        if 'role' in query_params:
            users_query, total_query = GinoQueryHelper.equal(
                RoleModel.name,
                query_params['role'],
                users_query,
                total_query
            )

        if 'display_name' in query_params:
            users_query, total_query = GinoQueryHelper.search(
                UserModel.display_name,
                query_params['display_name'],
                users_query,
                total_query
            )

        users_query = GinoQueryHelper.pagination(
            query_params, users_query
        )
        users_query = GinoQueryHelper.order(
            query_params,
            users_query, {
                'id': UserModel.id,
                'displayName': UserModel.display_name,
                'role': RoleModel.display_name,
            }
        )

        total = await total_query.gino.scalar()
        users = await users_query.gino.load(
            UserModel.distinct(UserModel.id).load(role=RoleModel)
        ).all()

        return make_list_response([user.jsonify() for user in users], total)

    @with_transaction
    @jwt_required
    @permissions.required(action=permissions.actions.CREATE)
    async def post(self, request):
        data = await request.json()
        if not await is_username_unique(data['username']):
            return make_error(
                f'User with username {data["username"]} already exist',
                status_code=400
            )

        try:
            role_id = await get_role_id(data)
        except RoleNotExist:
            return make_error("Role doesn't exist", status_code=404)

        new_user = await UserModel.create(
            username=data['username'],
            password=sha256.hash(data['password']),
            session=str(uuid4()),
            display_name=data['displayName'],
            email=data['email'],
            role_id=role_id,
            branch_id=data['branch_id'] if 'branch_id' in data else None
        )

        return make_response({'id': new_user.id})


class User(HTTPEndpoint):
    @staticmethod
    @jwt_required
    @permissions.required(action=permissions.actions.GET)
    async def get(request):
        user_id = request.path_params['user_id']
        users = (
            await UserModel
            .outerjoin(RoleModel)
            .outerjoin(BranchModel)
            .select()
            .where(
                UserModel.id == user_id
            )
            .gino.load(
                UserModel.distinct(
                    UserModel.id
                ).load(role=RoleModel, branch=BranchModel)
            ).all()
        )
        if users:
            return make_response(users[0].jsonify(for_card=True))
        return make_error(f'User with id {user_id} not found', status_code=404)

    @with_transaction
    @jwt_required
    @permissions.required(action=permissions.actions.UPDATE)
    async def patch(self, request):
        data = await request.json()
        user_id = request.path_params['user_id']
        user = await UserModel.get(user_id)
        if not user:
            return make_error(
                f'User with id {user_id} not found', status_code=404
            )

        try:
            role_id = await get_role_id(data)
        except RoleNotExist:
            return make_error("Role doesn't exist", status_code=404)

        values = {
            'display_name': data['displayName']
            if 'displayName' in data else None,
            'password': sha256.hash(data['password'])
            if 'password' in data else None,
            'deactivated': data['deactivated']
            if 'deactivated' in data else None,
            'email': data['email'] if 'email' in data else None,
            'role_id': role_id,
            'branch_id': data['branch_id'] if 'branch_id' in data else None
        }

        values = dict(filter(lambda item: item[1] is not None, values.items()))

        if values:
            await user.update(**values).apply()

        return NO_CONTENT


async def get_refresh_token(request):
    data = await request.json()
    user = await UserModel.get_by_identifier(data['identifier'])

    if not user:
        return make_error('User not found', status_code=404)

    if not sha256.verify(data['password'], user.password):
        return make_error('Wrong credentials', status_code=401)

    return make_response({
        'id': user.id,
        'email': user.email,
        'username': user.username,
        'refresh_token': create_refresh_token(user.session),
        'access_token': create_access_token(user.session)
    })


@jwt_required(token_type='refresh')
async def get_access_token(request, user):
    return make_response({
        'access_token': create_access_token(user.session),
    })


@jwt_required
async def reset_session(request, user):
    data = await request.json()

    if not sha256.verify(data['password'], user.password):
        return make_error('Wrong credentials', status_code=401)

    await user.update(
        session=str(uuid4())
    ).apply()

    return NO_CONTENT


@jwt_required
async def get_actions(request, user):
    return make_response(await permissions.get_actions(user.role_id))


routes = [
    Route('/', Users),
    Route('/{user_id:int}', User),
    Route('/actions', get_actions, methods=['GET']),
    Route('/reset-session', reset_session, methods=['POST']),
    Route('/access-tokens', get_access_token, methods=['POST']),
    Route('/refresh-tokens', get_refresh_token, methods=['POST']),
]
