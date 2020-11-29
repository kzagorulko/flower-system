import json
from starlette.routing import Route
from starlette.endpoints import HTTPEndpoint

from ..database import db
from ..models import BranchModel, UserModel
from ..utils import (
    jwt_required, make_error, with_transaction, Permissions, GinoQueryHelper,
    make_response, make_list_response, NO_CONTENT,
)
from .utils import is_address_unique

permissions = Permissions(app_name='branches')


class Branches(HTTPEndpoint):
    @staticmethod
    @jwt_required
    @permissions.required(action=permissions.actions.GET)
    async def get(request):
        branches_query = BranchModel.query
        total_query = db.select([db.func.count(BranchModel.id)])

        query_params = request.query_params

        if 'id' in query_params:
            ids = json.loads(query_params['id'])
            branches_query, total_query = GinoQueryHelper.in_(
                branches_query,
                total_query,
                BranchModel.id,
                ids
            )

        if 'address' in query_params:
            branches_query, total_query = GinoQueryHelper.search(
                BranchModel.address,
                query_params['address'],
                branches_query,
                total_query
            )

        branches_query = GinoQueryHelper.pagination(
            query_params, branches_query
        )
        branches_query = GinoQueryHelper.order(
            query_params,
            branches_query, {
                'id': BranchModel.id,
                'address': BranchModel.address,
            }
        )

        total = await total_query.gino.scalar()
        branches = await branches_query.gino.all()

        return make_list_response(
            [branch.jsonify() for branch in branches],
            total
        )

    @with_transaction
    @jwt_required
    @permissions.required(action=permissions.actions.CREATE)
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

        return make_response({'id': new_branch.id})


class Branch(HTTPEndpoint):

    @staticmethod
    @jwt_required
    @permissions.required(action=permissions.actions.GET_ONE)
    async def get(request):
        branch_id = request.path_params['branch_id']
        branches_query = (
            BranchModel
            .outerjoin(UserModel)
            .select()
        )
        branches_query = branches_query.where(
            BranchModel.id == branch_id
        )

        branches = await branches_query.gino.load(
            BranchModel.distinct(BranchModel.id).load(
                users=UserModel
            )
        ).all()

        if branches:
            return make_response(branches[0].jsonify(for_card=True))
        return make_error(description='Branch not found', status_code=404)

    @with_transaction
    @jwt_required
    @permissions.required(action=permissions.actions.UPDATE)
    async def patch(self, request):
        data = await request.json()
        branch_id = request.path_params['branch_id']
        branch = await BranchModel.get(branch_id)

        if not branch:
            return make_error(
                f'Branch with id {branch_id} not found', status_code=404
            )

        if 'address' in data:
            await branch.update(address=data['address']).apply()

        return NO_CONTENT


@jwt_required
async def get_actions(request, user):
    return make_response(await permissions.get_actions(user.role_id))


routes = [
    Route('/', Branches),
    Route('/{branch_id:int}', Branch),
    Route('/actions', get_actions, methods=['GET']),
]
