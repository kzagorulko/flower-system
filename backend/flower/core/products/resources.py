import json
from starlette.routing import Route
from starlette.endpoints import HTTPEndpoint

from ..database import db
from ..utils import (
    with_transaction, jwt_required, make_response, make_list_response,
    make_error, Permissions, GinoQueryHelper, MediaUtils, NO_CONTENT,
)
from ..models import ProductModel

permissions = Permissions(app_name='products')


class Products(HTTPEndpoint):
    @with_transaction
    @jwt_required
    @permissions.required(action=permissions.actions.CREATE)
    async def post(self, request):
        data = await request.json()

        try:
            image_file_base64 = data['image']
            name = data['name']
            price = float(data['price'])
            description = data['description']

            image_path = await MediaUtils.save_file_base64(image_file_base64)

            product = await ProductModel.create(
                name=name,
                image_path=image_path,
                price=price,
                description=description
            )

            return make_response({'id': product.id})

        except Exception as e:
            return make_error(
                e.args[0],
                status_code=400
            )

    @jwt_required
    @permissions.required(action=permissions.actions.GET)
    async def get(self, request):
        query_params = request.query_params

        current_query = ProductModel.query
        total_query = db.select([db.func.count(ProductModel.id)])

        if 'id' in query_params:
            ids = json.loads(query_params['id'])
            current_query = current_query.where(ProductModel.id.in_(ids))
            total_query = total_query.where(ProductModel.id.in_(ids))

        if 'name' in query_params:
            current_query = current_query.where(
                ProductModel.name.ilike(f'%{query_params["name"]}%')
            )

        current_query = GinoQueryHelper.pagination(
            query_params, current_query
        )
        current_query = GinoQueryHelper.order(
            query_params,
            current_query, {
                'id': ProductModel.id,
                'name': ProductModel.name,
                'price': ProductModel.price,
            }
        )

        total = await total_query.gino.scalar()
        products = await current_query.gino.all()

        return make_list_response(
            [product.jsonify() for product in products],
            total
        )


class Product(HTTPEndpoint):
    @with_transaction
    @jwt_required
    @permissions.required(action=permissions.actions.UPDATE)
    async def patch(self, request):
        product_id = request.path_params['product_id']
        data = await request.json()

        try:
            product = await ProductModel.get(product_id)

            if not product:
                raise Exception('Product not found')

            name = product.name
            image_path = product.image_path
            price = product.price
            description = product.description

            if 'image' in data:
                image_file_base64 = data['image']
                new_image_path = await MediaUtils.save_file_base64(
                    image_file_base64
                )

                MediaUtils.delete_file(image_path)
                image_path = new_image_path

            if 'name' in data:
                name = data['name']
            if 'price' in data:
                price = float(data['price'])
            if 'description' in data:
                description = data['description']

            await product.update(
                name=name,
                image_path=image_path,
                price=price,
                description=description
            ).apply()

            return NO_CONTENT

        except Exception as e:
            return make_error(
                e.args[0],
                status_code=400
            )

    @jwt_required
    @permissions.required(action=permissions.actions.GET)
    async def get(self, request):
        product_id = request.path_params['product_id']

        product = await ProductModel.get(product_id)

        if not product:
            return make_error(
                f'Product with id = {product_id} is not exist',
                status_code=404
            )

        return make_response(product.jsonify())


@jwt_required
async def get_actions(request, user):
    return make_response(await permissions.get_actions(user.role_id))


routes = [
    Route('/', Products),
    Route('/{product_id:int}', Product),
    Route('/actions', get_actions, methods=['GET']),
]
