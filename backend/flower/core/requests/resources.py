import datetime

from starlette.routing import Route
from starlette.endpoints import HTTPEndpoint

from ..database import db
from ..models import (
    RequestCategoryModel, RequestModel, UserModel, RoleModel,
    PermissionAction, RequestStatus as Status
)
from ..utils import (
    jwt_required, Permissions, make_error, with_transaction, convert_to_utc,
    GinoQueryHelper, make_response,  make_list_response,  NO_CONTENT,
)
from .utils import is_name_unique


permissions = Permissions(app_name='requests')


class Categories(HTTPEndpoint):
    @staticmethod
    @jwt_required(return_user=False)
    async def get(request):
        query_params = request.query_params

        query = RequestCategoryModel.query
        total_query = db.select([db.func.count(RequestCategoryModel.id)])

        if 'name' in query_params:
            query = query.where(
                RequestCategoryModel.name.ilike(f'%{query_params["name"]}%')
            )
            total_query = total_query.where(
                RequestCategoryModel.name.ilike(f'%{query_params["name"]}%')
            )

        query = GinoQueryHelper.pagination(
            query_params, query
        )

        query = GinoQueryHelper.order(
            query_params,
            query, {
                'id': RequestCategoryModel.id,
                'name': RequestCategoryModel.name,
            }
        )

        categories = await query.gino.all()
        total = await total_query.gino.scalar()

        return make_list_response(
            [category.jsonify() for category in categories],
            total
        )

    @with_transaction
    @jwt_required
    @permissions.required(action=PermissionAction.CREATE_CATEGORY)
    async def post(self, request):
        data = await request.json()

        if is_name_unique(data['name']):
            category = await RequestCategoryModel.create(
                name=data['name']
            )
            return make_response({'id': category.id})
        return make_error(
            f'Category with name {data["name"]} already exists'
        )


class Category(HTTPEndpoint):
    @jwt_required(return_user=False)
    async def get(self, request):
        category_id = request.path_params['category_id']
        category = await RequestCategoryModel.get(category_id)
        return make_response(category.jsonify())

    @with_transaction
    @jwt_required
    @permissions.required(action=PermissionAction.UPDATE_CATEGORY)
    async def patch(self, request):
        data = await request.json()
        category_id = request.path_params['category_id']

        category = await RequestCategoryModel.get(category_id)

        if category:
            if is_name_unique(data['name']):
                await category.update(name=data['name']).apply()
                return NO_CONTENT
            return make_error(
                f'Category with name {data["name"]} already exists'
            )
        return make_error(
            f'Category with id {category_id} not found', status_code=404
        )


class Requests(HTTPEndpoint):
    @jwt_required
    @permissions.required(
        action=PermissionAction.GET,
        return_user=True,
        return_role=True
    )
    async def get(self, request, user, role):
        query_params = request.query_params
        total_query = db.select([db.func.count(RequestModel.id)])

        requests_query = (
            RequestModel
            .outerjoin(RoleModel)
            .select()
        )

        if role.name != 'admin':
            permissions_where = (
                (RequestModel.executor_id == user.id)
                | (RequestModel.creator_id == user.id)
            )
            if role.name != 'branch':
                permissions_where |= (
                    RequestModel.department_id == user.role_id
                )
            requests_query = requests_query.where(permissions_where)
            total_query = total_query.where(permissions_where)

        if 'name' in query_params:
            requests_query, total_query = GinoQueryHelper.search(
                RequestModel.name, query_params['name'], requests_query,
                total_query
            )

        if 'view' in query_params:
            if query_params['view'] == 'INBOX':
                requests_query = requests_query.where(
                    RequestModel.department_id == user.role_id
                )
                total_query = total_query.where(
                    RequestModel.department_id == user.role_id
                )
            elif query_params['view'] == 'OUTBOX':
                requests_query = requests_query.where(
                    RequestModel.creator_id == user.id
                )
                total_query = total_query.where(
                    RequestModel.creator_id == user.id
                )
            elif query_params['view'] == 'EXECUTOR':
                requests_query = requests_query.where(
                    RequestModel.executor_id == user.id
                )
                total_query = total_query.where(
                    RequestModel.executor_id == user.id
                )

        requests_query = GinoQueryHelper.pagination(
            query_params, requests_query
        )

        requests_query = GinoQueryHelper.order(
            query_params,
            requests_query, {
                'id': RequestModel.id,
                'name': RequestModel.name,
                'department': RoleModel.display_name,
                'status': RequestModel.status,
                'created': RequestModel.created,
                'hasExecutor': RequestModel.executor_id,
            }
        )

        if 'noExecutor' in query_params:
            requests_query = requests_query.where(
                RequestModel.executor_id.is_(None)
            )
            total_query = total_query.where(RequestModel.executor_id.is_(None))

        total = await total_query.gino.scalar()
        requests = await requests_query.gino.load(
            RequestModel.distinct(RequestModel.id).load(department=RoleModel)
        ).all()

        return make_list_response(
            [_request.jsonify() for _request in requests],
            total
        )

    @with_transaction
    @jwt_required
    @permissions.required(action=PermissionAction.CREATE, return_user=True)
    async def post(self, request, user):
        data = await request.json()
        request = await RequestModel.create(
            name=data['name'],
            description=data['description'],
            created=convert_to_utc(datetime.datetime.now()),
            status=Status.NEW,
            creator_id=user.id,
            department_id=data['department_id'],
            category_id=data['category_id'],
        )
        return make_response({'id': request.id})


class Request(HTTPEndpoint):
    @jwt_required
    @permissions.required(
        action=PermissionAction.GET,
        return_role=True,
        return_user=True
    )
    async def get(self, request, role, user):
        request_id = request.path_params['request_id']

        ExecutorModel = UserModel.alias()
        ExecutorRoleModel = RoleModel.alias()
        CreatorRoleModel = RoleModel.alias()

        requests_query = (
            RequestModel
            .outerjoin(UserModel, RequestModel.creator_id == UserModel.id)
            .outerjoin(
                ExecutorModel, RequestModel.executor_id == ExecutorModel.id
            )
            .outerjoin(RoleModel, RequestModel.department_id == RoleModel.id)
            .outerjoin(RequestCategoryModel)
            .outerjoin(
                ExecutorRoleModel,
                ExecutorModel.role_id == ExecutorRoleModel.id
            )
            .outerjoin(
                CreatorRoleModel,
                UserModel.role_id == CreatorRoleModel.id
            )
            .select()
            .where(RequestModel.id == request_id)
        )

        if role.name != 'admin':
            permissions_where = (
                (RequestModel.executor_id == user.id)
                | (RequestModel.creator_id == user.id)
            )
            if role.name != 'branch':
                permissions_where |= (
                    RequestModel.department_id == user.role_id
                )
            requests_query = requests_query.where(permissions_where)

        requests = await requests_query.gino.load(
            RequestModel.distinct(RequestModel.id).load(
                category=RequestCategoryModel,
                department=RoleModel,
                creator=UserModel.load(role=CreatorRoleModel),
                executor=ExecutorModel.load(role=ExecutorRoleModel),
            )
        ).all()

        if requests:
            return make_response(requests[0].jsonify(for_card=True))
        return make_error(
            f'Request with id {request_id} not found', status_code=404
        )

    @with_transaction
    @jwt_required
    @permissions.required(action=PermissionAction.UPDATE, return_user=True)
    async def patch(self, request, user):
        request_id = request.path_params['request_id']
        system_request = await RequestModel.get(request_id)

        if system_request.executor_id:
            return make_error(
                'Request already has a executor', status_code=400
            )

        if user.role_id != system_request.department_id:
            return make_error(
                'Executor has wrong department', status_code=403
            )

        await system_request.update(
            executor_id=user.id, status=Status.IN_PROGRESS
        ).apply()

        return NO_CONTENT


class RequestStatus(HTTPEndpoint):
    @jwt_required
    @permissions.required(action=PermissionAction.UPDATE, return_user=True)
    async def patch(self, request, user):
        request_id = request.path_params['request_id']
        status = (await request.json())['status']

        system_request = await RequestModel.get(request_id)

        if system_request.executor_id != user.id:
            return make_error('User is not a executor', status_code=403)

        category_names = [category.name for category in Status]

        if status not in category_names:
            return make_error(f'Status {status} not found', status_code=404)

        await system_request.update(status=status).apply()

        return NO_CONTENT


@jwt_required
async def get_actions(request, user):
    return make_response(await permissions.get_actions(user.role_id))


routes = [
    Route('/', Requests),
    Route('/{request_id:int}', Request),
    Route('/{request_id:int}/status', RequestStatus),
    Route('/categories', Categories),
    Route('/categories/{category_id:int}', Category),
    Route('/actions', get_actions, methods=['GET']),
]
