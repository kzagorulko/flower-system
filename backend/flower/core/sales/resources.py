from starlette.routing import Route
from starlette.endpoints import HTTPEndpoint
from starlette.responses import JSONResponse

from datetime import datetime

from ..database import db
from ..utils import (
    with_transaction, jwt_required,
    make_error, Permissions, GinoQueryHelper, is_user_role_in
)
from ..utils import is_user_in_branch
from ..models import SalesModel, ProductModel, BranchModel

permissions = Permissions(app_name='sales')


class Sales(HTTPEndpoint):
    @with_transaction
    @jwt_required
    @permissions.required(action=permissions.actions.CREATE, return_user=True)
    async def post(self, request, user):
        data = await request.json()

        try:
            if 'value' not in data:
                raise Exception('Parameter "value" required')
            if 'product_id' not in data:
                raise Exception('Parameter "product_id" required')
            if 'branch_id' not in data:
                raise Exception('Parameter "branch_id" required')

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

            sale = await SalesModel.create(
                value=value,
                product_id=product.id,
                branch_id=branch.id,
                date=datetime.now()
            )

            return JSONResponse({'id': sale.id})

        except Exception as e:
            return make_error(
                e.args[0],
                status_code=400
            )

    @jwt_required
    @permissions.required(action=permissions.actions.GET)
    async def get(self, request):
        query_params = request.query_params

        current_query = SalesModel.query

        total_query = db.select([db.func.count(db.func.distinct(SalesModel.date_month_year))])

        # filtering
        if 'product_id' in query_params:
            current_query = current_query.where(
                SalesModel.product_id == int(query_params['product_id'])
            )
            total_query = total_query.where(
                SalesModel.product_id == int(query_params['product_id'])
            )
        if 'branch_id' in query_params:
            current_query = current_query.where(
                SalesModel.branch_id == int(query_params['branch_id'])
            )
            total_query = total_query.where(
                SalesModel.branch_id == int(query_params['branch_id'])
            )
        if 'year' in query_params and 'month' in query_params:
            current_query = current_query.where(
                (SalesModel.date_month == float(query_params['month'])) &
                (SalesModel.date_year == float(query_params['year'])))
            total_query = total_query.where(
                (SalesModel.date_month == float(query_params['month'])) &
                (SalesModel.date_year == float(query_params['year'])))

        current_query = GinoQueryHelper.pagination(
            query_params, current_query
        )

        sales = await current_query.gino.all()

        result = []
        current_date_group = {}  # словарь дла хранения кластера продаж

        # проходит по всем продажам, разбивая их на кластеры
        for sale in sales:

            if not current_date_group:
                current_date_group = {
                    "items": [],
                    "date": sale.date_month_year
                }

            # замыкаем кластер по месяцу и дате
            if sale.date_month_year != current_date_group['date']:
                result.append({
                    "date": current_date_group['date'].zfill(7),
                    "sales": current_date_group['items'],
                })
                current_date_group['date'] = sale.date_month_year
                current_date_group['items'] = []

            current_date_group['items'].append(sale.jsonify())

        # проверяем, нужно ли замкнуть кластер в последний раз
        if current_date_group['items']:
            result.append({
                "date": current_date_group['date'].zfill(7),
                "sales": current_date_group['items'],
            })

        total = await total_query.gino.scalar()

        return JSONResponse({
            'items': result,
            'total': total,
        })


class Sale(HTTPEndpoint):
    @jwt_required
    @permissions.required(action=permissions.actions.GET)
    async def get(self, request):
        sale_id = request.path_params['sale_id']

        sale = (
            await SalesModel
            .outerjoin(ProductModel)
            .outerjoin(BranchModel)
            .select()
            .where(
                SalesModel.id == sale_id
            )
            .gino.load(
                SalesModel.distinct(
                    SalesModel.id
                ).load(product=ProductModel, branch=BranchModel)
            ).first()
        )

        return JSONResponse({
            'items': sale.jsonify(for_card=True)
        })


@jwt_required
async def get_actions(request, user):
    return JSONResponse(await permissions.get_actions(user.role_id))


routes = [
    Route('/', Sales),
    Route('/{sale_id:int}', Sale),
    Route('/actions', get_actions, methods=['GET']),
]
