from starlette.routing import Route
from starlette.endpoints import HTTPEndpoint

from pytz import utc
from datetime import datetime

from ..database import db
from ..utils import (
    check_missing_params,
    with_transaction, jwt_required, make_response, make_list_response,
    make_error, Permissions, GinoQueryHelper, NO_CONTENT, PermissionAction
)
from ..models import (
    WarehouseModel, ProductModel, ProductWarehouseModel,
    PurchaseStatus as Status, PurchaseModel, ContractModel, ContractStatus,
    SupplyModel, SupplyStatus
)

permissions = Permissions(app_name='purchases')


class Purchases(HTTPEndpoint):
    @with_transaction
    @jwt_required
    @permissions.required(action=permissions.actions.CREATE)
    async def post(self, request):
        data = await request.json()

        try:
            check_missing_params(
                data,
                [
                    'value',
                    'product_id',
                    'warehouse_id',
                    'date',
                    'address',
                    'contract_id',
                ]
            )

            product = await ProductModel.get(data['product_id'])
            warehouse = await WarehouseModel.get(data['warehouse_id'])
            contract = await ContractModel.get(data['contract_id'])

            target_date = datetime.strptime(data['date'], '%Y-%m-%d')

            if not product:
                raise Exception('Product not found')

            if not warehouse:
                raise Exception('Warehouse not found')

            if not contract or contract.status != ContractStatus.OPERATING:
                raise Exception('Contract is not valid')

            products_in_warehouse = await db.select(
                [db.func.sum(ProductWarehouseModel.value)]
            ).where(
                ProductWarehouseModel.warehouse_id == warehouse.id
            ).gino.scalar() or 0

            purchases_in_progress = await db.select(
                [db.func.sum(PurchaseModel.value)]
            ).where(
                (
                    (PurchaseModel.status == Status.NEW) |
                    (PurchaseModel.status == Status.IN_PROGRESS)
                ) &
                (PurchaseModel.date <= target_date)
            ).gino.scalar() or 0

            supplies = await db.select(
                [db.func.sum(SupplyModel.value)]
            ).where(
                (
                    (SupplyModel.status != SupplyStatus.CANCELLED)
                    & (SupplyModel.date < target_date)
                )
            ).gino.scalar() or 0

            if (
                products_in_warehouse + purchases_in_progress - supplies
                + int(data['value'])
                > warehouse.max_value
            ):
                raise Exception('Warehouse limit will be reached')

            purchase = await PurchaseModel.create(
                value=data['value'],
                product_id=product.id,
                warehouse_id=warehouse.id,
                status=Status.NEW,
                address=data['address'],
                date=target_date.astimezone(utc),
                contract_id=contract.id,
            )

            return make_response({'id': purchase.id})
        except Exception as e:
            return make_error(
                e.args[0],
                status_code=400
            )

    @jwt_required
    @permissions.required(action=permissions.actions.GET)
    async def get(self, request):
        query_params = request.query_params

        current_query = PurchaseModel.query
        total_query = db.select([db.func.count(PurchaseModel.id)])

        if 'product_id' in query_params:
            current_query, total_query = GinoQueryHelper.equal(
                PurchaseModel.product_id,
                int(query_params['product_id']),
                current_query,
                total_query
            )
        if 'warehouse_id' in query_params:
            current_query, total_query = GinoQueryHelper.equal(
                PurchaseModel.warehouse_id,
                int(query_params['warehouse_id']),
                current_query,
                total_query
            )

        if 'contract_id' in query_params:
            current_query, total_query = GinoQueryHelper.equal(
                PurchaseModel.contract_id,
                int(query_params['contract_id']),
                current_query,
                total_query
            )

        if 'startDate' in query_params:
            current_query, total_query = GinoQueryHelper.month_year_cond(
                PurchaseModel.date,
                query_params['startDate'],
                GinoQueryHelper.GTE,
                current_query,
                total_query
            )
        if 'endDate' in query_params:
            current_query, total_query = GinoQueryHelper.month_year_cond(
                PurchaseModel.date,
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
                'id': PurchaseModel.id,
                'value': PurchaseModel.value,
                'date': PurchaseModel.date
            }
        )

        total = await total_query.gino.scalar()
        items = await current_query.gino.all()

        return make_list_response(
            [item.jsonify() for item in items],
            total
        )


class Purchase(HTTPEndpoint):
    @staticmethod
    @jwt_required
    @permissions.required(action=permissions.actions.GET)
    async def get(request):
        purchase_id = request.path_params['purchase_id']

        purchase = await PurchaseModel.get(purchase_id)

        if purchase:
            return make_response(purchase.jsonify())
        return make_error(description='Purchase not found', status_code=404)


class PurchaseStatus(HTTPEndpoint):
    @with_transaction
    @jwt_required
    @permissions.required(
        action=PermissionAction.UPDATE_STATUS, return_role=True
    )
    async def patch(self, request, role):
        purchase_id = request.path_params['purchase_id']
        status = (await request.json())['status']

        purchase = await PurchaseModel.get(purchase_id)

        category_names = [category.name for category in Status]

        if status not in category_names:
            return make_error(f'Status {status} not found', status_code=404)

        # если закупка объявляется выполненной, то добавляем продукт на склад
        # проверка на кол-во продукта не производится,
        # т.к. это полностью регулируется
        # создании закупки
        if (
                status == Status.DONE.name and purchase.status != Status.DONE
                and role.name in ('admin', 'logistics_department')
        ):
            product_in_warehouse = await ProductWarehouseModel.query.where(
                (ProductWarehouseModel.warehouse_id == purchase.warehouse_id) &
                (ProductModel.id == purchase.product_id)
            ).gino.first()

            if not product_in_warehouse:
                await ProductWarehouseModel.create(
                    value=purchase.value,
                    product_id=purchase.product_id,
                    warehouse_id=purchase.warehouse_id
                )
            else:
                new_value = product_in_warehouse.value + purchase.value
                await product_in_warehouse.update(value=new_value).apply()

        await purchase.update(status=status).apply()

        return NO_CONTENT


class PurchaseWarehouse(HTTPEndpoint):
    @with_transaction
    @jwt_required
    @permissions.required(action=PermissionAction.UPDATE_WAREHOUSE)
    async def patch(self, request):
        purchase_id = request.path_params['purchase_id']
        warehouse_id = (await request.json())['warehouse_id']

        purchase = await PurchaseModel.get(purchase_id)

        if purchase and purchase.status == Status.NEW:
            await purchase.update(warehouse_id=warehouse_id).apply()

            return NO_CONTENT

        return make_error('Status of purchase is not `NEW`')


@jwt_required
async def get_actions(request, user):
    return make_response(await permissions.get_actions(user.role_id))


routes = [
    Route('/', Purchases),
    Route('/{purchase_id:int}', Purchase),
    Route('/{purchase_id:int}/status', PurchaseStatus),
    Route('/{purchase_id:int}/warehouse', PurchaseWarehouse),
    Route('/actions', get_actions, methods=['GET']),
]
