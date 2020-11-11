from uuid import uuid4

from starlette.routing import Route
from starlette.endpoints import HTTPEndpoint
from starlette.responses import JSONResponse, Response
from passlib.hash import pbkdf2_sha256 as sha256

from ..database import db
from ..utils import (
    with_transaction, create_refresh_token, create_access_token, jwt_required,
    make_error, Permissions
)
from ..models import UserModel, RoleModel, UserBranchModel, BranchModel
from .utils import (
    is_username_unique, get_role_id, RoleNotExist,
    get_column_for_order, change_branches
)

permissions = Permissions(app_name='users')


class Users(HTTPEndpoint):
    @staticmethod
    @jwt_required
    @permissions.required(action='get')
    async def get(request):
        users_query = UserModel.outerjoin(
            RoleModel
        ).outerjoin(UserBranchModel).select()
        total_query = db.select([db.func.count(UserModel.id)])

        query_params = request.query_params

        if 'display_name' in query_params:
            users_query = users_query.where(
                UserModel.display_name.ilike(
                    f'%{query_params["display_name"]}%'
                )
            )
            total_query = total_query.where(
                UserModel.display_name.ilike(
                    f'%{query_params["display_name"]}%'
                )
            )

        if 'branch' in query_params:
            users_query = users_query.where(
                BranchModel.address.ilike(
                    f'%{query_params["branch"]}%'
                )
            )
            total_query = total_query.where(
                BranchModel.address.ilike(
                    f'%{query_params["branch"]}%'
                )
            )

        if 'page' in query_params and 'perPage' in query_params:
            page = int(query_params['page']) - 1
            per_page = int(query_params['perPage'])
            users_query = users_query.limit(per_page).offset(page * per_page)

        if 'order' in query_params and 'field' in query_params:
            users_query = users_query.order_by(
                get_column_for_order(
                    query_params['field'],
                    query_params['order'] == 'ASC'
                )
            )

        total = await total_query.gino.scalar()
        users = await users_query.gino.load(
            UserModel.distinct(UserModel.id).load(
                role=RoleModel, branch=UserBranchModel
            )
        ).all()

        return JSONResponse({
            'items': [user.jsonify() for user in users],
            'total': total,
        })

    # TODO make this for admin only
    @with_transaction
    @jwt_required
    @permissions.required(action='create')
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
            role_id=role_id
        )
        if data['branches']:
            await change_branches(data['branches'], new_user.id)

        return JSONResponse({'id': new_user.id})


class User(HTTPEndpoint):
    @staticmethod
    @jwt_required
    @permissions.required(action='get')
    async def get(request):
        user_id = request.path_params['user_id']
        users = await UserModel.outerjoin(
            RoleModel
        ).outerjoin(UserBranchModel).select().where(
            UserModel.id == user_id
        ).gino.load(
            UserModel.distinct(
                UserModel.id
            ).load(role=RoleModel, branches=UserBranchModel)
        ).all()
        if users:
            return JSONResponse(users[0].jsonify(for_card=True))
        return make_error(f'User with id {user_id} not found', status_code=404)

    # TODO: make this method for admin only

    @with_transaction
    @jwt_required
    @permissions.required(action='update')
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

        if 'branches' in data:
            await change_branches(data['branches'], user_id)

        values = {
            'display_name': data['displayName']
            if 'displayName' in data else None,
            'password': sha256.hash(data['password'])
            if 'password' in data else None,
            'deactivated': data['deactivated']
            if 'deactivated' in data else None,
            'email': data['email'] if 'email' in data else None,
            'role_id': role_id
        }

        values = dict(filter(lambda item: item[1] is not None, values.items()))

        if values:
            await user.update(**values).apply()

        return Response('', status_code=204)


async def get_refresh_token(request):
    data = await request.json()
    user = await UserModel.get_by_identifier(data['identifier'])

    if not user:
        return make_error('User not found', status_code=404)

    if not sha256.verify(data['password'], user.password):
        return make_error('Wrong credentials', status_code=401)

    return JSONResponse({
        'id': user.id,
        'email': user.email,
        'username': user.username,
        'refresh_token': create_refresh_token(user.session),
        'access_token': create_access_token(user.session)
    })


@jwt_required(token_type='refresh')
async def get_access_token(request, user):
    return JSONResponse({
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

    return Response('', status_code=204)


@jwt_required
async def get_actions(request, user):
    return JSONResponse(await permissions.get_actions(user.role_id))


routes = [
    Route('/', Users),
    Route('/{user_id:int}', User),
    Route('/actions', get_actions, methods=['GET']),
    Route('/reset-session', reset_session, methods=['POST']),
    Route('/access-tokens', get_access_token, methods=['POST']),
    Route('/refresh-tokens', get_refresh_token, methods=['POST']),
]
