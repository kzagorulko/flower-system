from starlette.routing import Route
from starlette.endpoints import HTTPEndpoint

from datetime import datetime, date
from calendar import monthrange

from ..database import db
from ..utils import (
    with_transaction, jwt_required,  is_user_in_branch, make_list_response,
    make_error, Permissions, GinoQueryHelper, is_user_role_in, make_response,
    convert_to_utc,
)
from ..models import SaleModel, ProductModel, BranchModel

permissions = Permissions(app_name='sales')


class Sales(HTTPEndpoint):
    @with_transaction
    @jwt_required
    @permissions.required(action=permissions.actions.CREATE, return_user=True)
    async def post(self, request, user):
        data = await request.json()

        try:
            value = float(data['value'])
            product_id = data['product_id']
            branch_id = data['branch_id']

            product = await ProductModel.get(product_id)
            branch = await BranchModel.get(branch_id)

            if not product:
                raise Exception('Product not found')
            elif not branch:
                raise Exception('Branch not found')

            if (
                not await is_user_role_in(
                    user, ['admin']
                ) and
                not await is_user_in_branch(user, branch)
            ):
                raise Exception('User not in branch')

            sale = await SaleModel.create(
                value=value,
                product_id=product.id,
                branch_id=branch.id,
                date=convert_to_utc(datetime.now())
            )

            return make_response({'id': sale.id})

        except Exception as e:
            return make_error(
                e.args[0],
                status_code=400
            )

    @jwt_required
    @permissions.required(
        action=permissions.actions.GET,
        return_role=True,
        return_user=True
    )
    async def get(self, request, user, role):
        query_params = request.query_params

        current_query = SaleModel.query

        total_query = db.select([db.func.count(SaleModel.id)])

        if 'product_id' in query_params:
            current_query = current_query.where(
                SaleModel.product_id == int(query_params['product_id'])
            )
            total_query = total_query.where(
                SaleModel.product_id == int(query_params['product_id'])
            )
        if 'branch_id' in query_params:
            current_query = current_query.where(
                SaleModel.branch_id == int(query_params['branch_id'])
            )
            total_query = total_query.where(
                SaleModel.branch_id == int(query_params['branch_id'])
            )
        if 'startDate' in query_params:
            year, month = query_params['startDate'].split('-')[:2]
            start_date = date(int(year), int(month), 1)
            current_query = current_query.where(
                SaleModel.date >= start_date
            )
            total_query = total_query.where(
                SaleModel.date >= start_date
            )
        if 'endDate' in query_params:
            year, month = query_params['endDate'].split('-')[:2]
            num_days = monthrange(int(year), int(month))[1]
            end_date = date(int(year), int(month), num_days)
            current_query = current_query.where(
                SaleModel.date <= end_date
            )
            total_query = total_query.where(
                SaleModel.date <= end_date
            )

        if role.name == 'branches':
            current_query = current_query.where(
                SaleModel.branch_id == user.branch_id
            )
            total_query = total_query.where(
                SaleModel.branch_id == user.branch_id
            )

        current_query = GinoQueryHelper.pagination(
            query_params, current_query
        )

        current_query = GinoQueryHelper.order(
            query_params,
            current_query,
            {
                'date_month_year': SaleModel.date_month_year,
                'date': SaleModel.date,
                'value': SaleModel.value,
                'product_id': SaleModel.product_id,
                'branch_id': SaleModel.branch_id,
                'id': SaleModel.id,
            }
        )

        sales = await current_query.gino.all()

        total = await total_query.gino.scalar()

        return make_list_response([sale.jsonify() for sale in sales], total)


class Sale(HTTPEndpoint):
    @jwt_required
    @permissions.required(action=permissions.actions.GET)
    async def get(self, request):
        sale_id = request.path_params['sale_id']

        sale = await SaleModel.get(sale_id)
        return make_response(sale.jsonify())


@jwt_required
async def get_actions(request, user):
    return make_response(await permissions.get_actions(user.role_id))


routes = [
    Route('/', Sales),
    Route('/{sale_id:int}', Sale),
    Route('/actions', get_actions, methods=['GET']),
]
