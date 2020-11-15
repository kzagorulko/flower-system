from ..models import RequestCategoryModel, RequestModel, RoleModel


async def is_name_unique(name):
    category = await RequestCategoryModel.query.where(
        RequestCategoryModel.name == name
    ).gino.first()
    if category:
        return False
    return True


def get_column_for_order(column_name, asc=True):
    names_x_columns = {
        'id': RequestModel.id,
        'name': RequestModel.name,
        'departament': RoleModel.display_name,
        'status': RequestModel.status,
        'created': RequestModel.created,
    }

    if asc:
        return names_x_columns[column_name]
    return names_x_columns[column_name].desc()
