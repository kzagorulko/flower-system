from ..database import db
from ..models import ProductWarehouseModel


async def change_products(products, warehouse_id, is_create=False):
    products = products
    product_ids = [product['id'] for product in products]

    if len(products) == 0:
        await ProductWarehouseModel.delete.where(
            ProductWarehouseModel.warehouse_id == warehouse_id
        ).gino.status()
    else:
        products_exist = await ProductWarehouseModel.query.where(
            (ProductWarehouseModel.warehouse_id == warehouse_id)
            & (ProductWarehouseModel.product_id.in_(product_ids))
        ).gino.all()

        count = await db.select(
            [db.func.count(ProductWarehouseModel.product_id)]
        ).where(
            ProductWarehouseModel.warehouse_id == warehouse_id
        ).gino.scalar()

        if len(products_exist) != len(products) or count != len(products):
            if not is_create:
                await ProductWarehouseModel.delete.where(
                    (ProductWarehouseModel.warehouse_id == warehouse_id) &
                    ~ (ProductWarehouseModel.product_id.in_(product_ids))
                ).gino.status()

            models_ids = [model.product_id for model in products_exist]

            result = []

            for product in products:
                if product["id"] not in models_ids:
                    result.append({
                        'warehouse_id': warehouse_id,
                        'product_id': product["id"],
                        'value': product["value"]
                    })

            if result:
                await ProductWarehouseModel.insert().gino.all(result)
