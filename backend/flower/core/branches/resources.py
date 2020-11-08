from starlette.responses import JSONResponse, Response
from starlette.routing import Route
from starlette.endpoints import HTTPEndpoint

from ..utils import jwt_required, make_error, with_transaction, Permissions
from ..models import BranchModel

from .utils import is_address_unique, get_column_for_order

from ..database import db

permissions = Permissions(app_name='branches')


class Branches(HTTPEndpoint):
    @staticmethod
    @jwt_required
    @permissions.required(action='get')
    async def get(self, request):
        branches_query = BranchModel.query
        total_query = db.select([db.func.count(BranchModel.id)])

        query_params = request.query_params

        if 'search' in query_params:
            branches_query.where(
                BranchModel.display_name.ilike(f'%{query_params["search"]}%')
            )

        if 'page' in query_params and 'perPage' in query_params:
            page = int(query_params['page']) - 1
            per_page = int(query_params['perPage'])
            branches_query = branches_query.limit(per_page).offset(page * per_page)

        if 'order' in query_params and 'field' in query_params:
            branches_query = branches_query.order_by(
                get_column_for_order(
                    query_params['field'],
                    query_params['order'] == 'ASC'
                )
            )

        total = await total_query.gino.scalar()
        branches = await branches_query.gino.all()

        return JSONResponse({
            'items': [branch.jsonify() for branch in branches],
            'total': total,
        })

    @staticmethod
    @with_transaction
    @jwt_required
    @permissions.required(action='create')
    async def post(self, request):
        data = await request.json()
        if not await is_address_unique(data['address']):
            return make_error(
                f'Branch with address {data["address"]} already exist',
                status_code=400
            )

        new_branch = await BranchModel.create(
            address=data['address']
        )

        return JSONResponse({'id': new_branch.id})


class Branch(HTTPEndpoint):
    @staticmethod
    @jwt_required
    @permissions.required(action='get')
    async def get(request):
        branch_id = request.path_params['branch_id']
        branch = await BranchModel.get(branch_id)
        if branch:
            return JSONResponse(branch.jsonify(for_card=True))
        return make_error(description='Branch not found', status_code=404)

    @staticmethod
    @with_transaction
    @jwt_required
    @permissions.required(action='update')
    async def patch(self, request):
        data = await request.json()
        branch_id = request.path_params['id']
        branch = await BranchModel.get(branch_id)

        if not branch:
            return make_error(
                f'Branch with id {branch_id} not found', status_code=404
            )

        values = {
            'address': data['address']
            if 'address' in data else None,
        }

        values = dict(filter(lambda item: item[1] is not None, values.items()))

        await branch.update(**values).apply()

        return Response('', status_code=204)


@jwt_required
async def get_actions(request, user):
    return JSONResponse(await permissions.get_actions(user.role_id))


routes = [
    Route('/', Branches),
    Route('/{branch_id:int}', Branch),
]
