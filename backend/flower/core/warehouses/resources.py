from starlette.routing import Route
from starlette.endpoints import HTTPEndpoint

from ..database import db
from ..utils import (
    validate_query_params,
    with_transaction, jwt_required, make_response, make_list_response,
    make_error, Permissions, GinoQueryHelper, NO_CONTENT,
)
from ..models import WarehouseModel, ProductWarehouseModel
from .utils import change_products

permissions = Permissions(app_name='warehouses')


class Warehouses(HTTPEndpoint):
    @with_transaction
    @jwt_required
    @permissions.required(action=permissions.actions.CREATE)
    async def post(self, request):
        data = await request.json()

        try:
            validate_query_params(data, ['address', 'max_value'])

            warehouse = await WarehouseModel.create(
                address=data['address'],
                max_value=data['max_value'],
            )

            if 'products' in data:
                await change_products(data['products'], warehouse.id, True)

            return make_response({'id': warehouse.id})
        except Exception as e:
            return make_error(
                e.args[0],
                status_code=400
            )

    @jwt_required
    @permissions.required(action=permissions.actions.GET)
    async def get(self, request):
        query_params = request.query_params

        current_query = WarehouseModel.query
        total_query = db.select([db.func.count(WarehouseModel.id)])

        if 'address' in query_params:
            current_query, total_query = GinoQueryHelper.search(
                WarehouseModel.address,
                query_params['address'],
                current_query,
                total_query
            )
        if 'max_value' in query_params:
            current_query, total_query = GinoQueryHelper.search(
                WarehouseModel.product_id,
                query_params['max_value'],
                current_query,
                total_query
            )

        current_query = GinoQueryHelper.pagination(
            query_params, current_query
        )
        current_query = GinoQueryHelper.order(
            query_params,
            current_query, {
                'id': WarehouseModel.id,
                'address': WarehouseModel.address,
                'max_value': WarehouseModel.max_value
            }
        )

        total = await total_query.gino.scalar()
        items = await current_query.gino.all()

        return make_list_response(
            [item.jsonify() for item in items],
            total
        )


class Warehouse(HTTPEndpoint):
    @staticmethod
    @jwt_required
    @permissions.required(action=permissions.actions.GET)
    async def get(request):
        warehouse_id = request.path_params['warehouse_id']
        current_query = (
            WarehouseModel
            .outerjoin(ProductWarehouseModel)
            .select()
        )
        current_query = current_query.where(
            WarehouseModel.id == warehouse_id
        )

        warehouses = await current_query.gino.load(
            WarehouseModel.distinct(WarehouseModel.id).load(
                products=ProductWarehouseModel
            )
        ).all()

        if warehouses:
            return make_response(warehouses[0].jsonify(for_card=True))
        return make_error(description='Warehouse not found', status_code=404)

    @with_transaction
    @jwt_required
    @permissions.required(action=permissions.actions.UPDATE)
    async def patch(self, request):
        data = await request.json()
        warehouse_id = request.path_params['warehouse_id']
        warehouse = await WarehouseModel.get(warehouse_id)

        if not warehouse:
            return make_error(
                f'Warehouse with id {warehouse_id} not found', status_code=404
            )

        if 'address' in data:
            await warehouse.update(address=data['address']).apply()

        if 'max_value' in data:
            await warehouse.update(address=data['max_value']).apply()

        if 'products' in data:
            await change_products(data['products'], warehouse_id)

        return NO_CONTENT


@jwt_required
async def get_actions(request, user):
    return make_response(await permissions.get_actions(user.role_id))


routes = [
    Route('/', Warehouses),
    Route('/{warehouse_id:int}', Warehouse),
    Route('/actions', get_actions, methods=['GET']),
]
