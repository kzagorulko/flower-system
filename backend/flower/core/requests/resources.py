import datetime

from starlette.routing import Route
from starlette.endpoints import HTTPEndpoint
from starlette.responses import JSONResponse, Response

from ..database import db
from ..models import (
    RequestCategoryModel, RequestModel, UserModel, RoleModel,
)
from ..utils import (
    jwt_required, Permissions, make_error, with_transaction, convert_to_utc,
)
from .utils import is_name_unique, get_column_for_order


permissions = Permissions(app_name='requests')


class Categories(HTTPEndpoint):
    @staticmethod
    @jwt_required(return_user=False)
    async def get(request):
        params = request.query_params

        query = RequestCategoryModel.query
        if 'name' in params:
            query = query.where(
                RequestCategoryModel.name.ilike(f'%{params["name"]}%')
            )

        categories = await query.gino.all()

        return JSONResponse({
            'categories': [category.jsonify() for category in categories]
        })

    @with_transaction
    @jwt_required
    @permissions.required(action='create_category')
    async def post(self, request):
        data = await request.json()

        if is_name_unique(data['name']):
            category = await RequestCategoryModel.create(
                name=data['name']
            )
            return JSONResponse({'id': category.id})
        return make_error(
            f'Category with name {data["name"]} already exists'
        )


class Category(HTTPEndpoint):
    @with_transaction
    @jwt_required
    @permissions.required(action='update_category')
    async def patch(self, request):
        data = await request.json()
        category_id = request.path_params['category_id']

        category = await RequestCategoryModel.get(category_id)

        if category:
            if is_name_unique(data['name']):
                await category.update(name=data['name']).apply()
                return Response('', 204)
            return make_error(
                f'Category with name {data["name"]} already exists'
            )
        return make_error(
            f'Category with id {category_id} not found', status_code=404
        )


class Requests(HTTPEndpoint):
    @jwt_required
    @permissions.required(action='get', return_user=True, return_role=True)
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
                    RequestModel.departament_id == user.role_id
                )
            requests_query = requests_query.where(permissions_where)

        if 'name' in query_params:
            requests_query = requests_query.where(
                RequestModel.name.ilike(
                    f'%{query_params["name"]}%'
                )
            )
            total_query = total_query.where(
                RequestModel.name.ilike(
                    f'%{query_params["name"]}%'
                )
            )

        if 'page' in query_params and 'perPage' in query_params:
            page = int(query_params['page']) - 1
            per_page = int(query_params['perPage'])
            requests_query = requests_query.limit(
                per_page
            ).offset(page * per_page)

        if 'order' in query_params and 'field' in query_params:
            requests_query = requests_query.order_by(
                get_column_for_order(
                    query_params['field'],
                    query_params['order'] == 'ASC'
                )
            )

        total = await total_query.gino.scalar()
        requests = await requests_query.gino.load(
            RequestModel.distinct(RequestModel.id).load(departament=RoleModel)
        ).all()

        return JSONResponse({
            'items': [_request.jsonify() for _request in requests],
            'total': total
        })

    @with_transaction
    @jwt_required
    @permissions.required(action='create', return_user=True)
    async def post(self, request, user):
        data = await request.json()
        request = await RequestModel.create(
            name=data['name'],
            description=data['description'],
            created=convert_to_utc(datetime.datetime.now()),
            status='NEW',
            creator_id=user.id,
            departament_id=data['departament_id'],
            category_id=data['category_id'],
        )
        return JSONResponse({'id': request.id})


class Request(HTTPEndpoint):
    @jwt_required
    @permissions.required(action='get', return_role=True, return_user=True)
    async def get(self, request, role, user):
        request_id = request.path_params['request_id']

        ExecutorModel = UserModel.alias()

        requests_query = (
            RequestModel
            .outerjoin(UserModel, RequestModel.creator_id == UserModel.id)
            .outerjoin(
                ExecutorModel, RequestModel.executor_id == ExecutorModel.id
            )
            .outerjoin(RoleModel, RequestModel.departament_id == RoleModel.id)
            .outerjoin(RequestCategoryModel)
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
                    RequestModel.departament_id == user.role_id
                )
            requests_query = requests_query.where(permissions_where)

        requests = await requests_query.gino.load(
            RequestModel.distinct(RequestModel.id).load(
                category=RequestCategoryModel,
                departament=RoleModel,
                creator=UserModel,
                executor=ExecutorModel,
            )
        ).all()

        if requests:
            return JSONResponse(requests[0].jsonify(for_card=True))
        return make_error(
            f'Request with id {request_id} not found', status_code=404
        )


routes = [
    Route('/', Requests),
    Route('/{request_id:int}', Request),
    Route('/categories', Categories),
    Route('/categories/{category_id:int}', Category),
]
