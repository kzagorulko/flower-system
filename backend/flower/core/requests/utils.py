from ..models import RequestCategoryModel


async def is_name_unique(name):
    category = await RequestCategoryModel.query.where(
        RequestCategoryModel.name == name
    ).gino.first()
    if category:
        return False
    return True
