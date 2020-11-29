from starlette.routing import Route
from starlette.endpoints import HTTPEndpoint

from pytz import utc
from datetime import datetime

from ..database import db
from ..utils import (
    validate_query_params,
    with_transaction, jwt_required, make_response, make_list_response,
    make_error, Permissions, GinoQueryHelper
)
from ..models import (
    WarehouseModel, ProductModel, ProductWarehouseModel,
    SupplyModel
)

permissions = Permissions(app_name='supplies')


class Supplies(HTTPEndpoint):
    @with_transaction
    @jwt_required
    @permissions.required(action=permissions.actions.CREATE)
    async def post(self, request):
        data = await request.json()

        try:
            validate_query_params(
                data,
                ['value', 'product_id', 'warehouse_id', 'branch_id']
            )

            product = await ProductModel.get(data['product_id'])
            warehouse = await WarehouseModel.get(data['warehouse_id'])
            branch = await WarehouseModel.get(data['branch_id'])

            if not product:
                raise Exception('Product not found')

            if not warehouse:
                raise Exception('Warehouse not found')

            if not branch:
                raise Exception('Branch not found')

            product_in_warehouse = await ProductWarehouseModel.query.where(
                (ProductWarehouseModel.warehouse_id == warehouse.id) &
                (ProductModel.id == product.id)
            ).gino.first()

            if not product_in_warehouse:
                raise Exception('Product in warehouse not found')

            if (
                product_in_warehouse.value - int(data['value']) < 0
            ):
                raise Exception('Insufficient quantity of goods in stock')

            new_value = product_in_warehouse.value - int(data['value'])

            await product_in_warehouse.update(value=new_value).apply()

            supply = await SupplyModel.create(
                value=data['value'],
                product_id=product.id,
                warehouse_id=warehouse.id,
                branch_id=branch.id,
                date=datetime.now().astimezone(utc),
            )

            return make_response({'id': supply.id})
        except Exception as e:
            return make_error(
                e.args[0],
                status_code=400
            )

    @jwt_required
    @permissions.required(action=permissions.actions.GET)
    async def get(self, request):
        query_params = request.query_params

        current_query = SupplyModel.query
        total_query = db.select([db.func.count(SupplyModel.id)])

        if 'product_id' in query_params:
            current_query, total_query = GinoQueryHelper.equal(
                SupplyModel.product_id,
                int(query_params['product_id']),
                current_query,
                total_query
            )
        if 'warehouse_id' in query_params:
            current_query, total_query = GinoQueryHelper.equal(
                SupplyModel.warehouse_id,
                int(query_params['warehouse_id']),
                current_query,
                total_query
            )
        if 'branch_id' in query_params:
            current_query, total_query = GinoQueryHelper.equal(
                SupplyModel.branch_id,
                int(query_params['branch_id']),
                current_query,
                total_query
            )

        if 'startDate' in query_params:
            current_query, total_query = GinoQueryHelper.month_year_cond(
                SupplyModel.date,
                query_params['startDate'],
                GinoQueryHelper.GTE,
                current_query,
                total_query
            )
        if 'endDate' in query_params:
            current_query, total_query = GinoQueryHelper.month_year_cond(
                SupplyModel.date,
                query_params['endDate'],
                GinoQueryHelper.LTE,
                current_query,
                total_query
            )

        current_query = GinoQueryHelper.pagination(
            query_params, current_query
        )
        current_query = GinoQueryHelper.order(
            query_params,
            current_query, {
                'id': SupplyModel.id,
                'value': SupplyModel.value,
                'date': SupplyModel.date
            }
        )

        total = await total_query.gino.scalar()
        items = await current_query.gino.all()

        return make_list_response(
            [item.jsonify() for item in items],
            total
        )


class Supply(HTTPEndpoint):
    @staticmethod
    @jwt_required
    @permissions.required(action=permissions.actions.GET_ONE)
    async def get(request):
        supply_id = request.path_params['supply_id']

        supply = await SupplyModel.query.where(
            SupplyModel.id == supply_id
        ).gino.first()

        if supply:
            return make_response(supply.jsonify())
        return make_error(description='Supply not found', status_code=404)


@jwt_required
async def get_actions(request, user):
    return make_response(await permissions.get_actions(user.role_id))


routes = [
    Route('/', Supplies),
    Route('/{supply_id:int}', Supply),
    Route('/actions', get_actions, methods=['GET']),
]