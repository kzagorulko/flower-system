from ..models import ProviderModel


async def is_name_unique(name):
    provider = await ProviderModel.query.where(
        ProviderModel.name == name
    ).gino.first()
    if provider:
        return False
    return True


def get_column_for_order(column_name, asc=True):
    names_x_columns = {
        'id': ProviderModel.id,
        'name': ProviderModel.name,
        'status': ProviderModel.status,
    }

    if asc:
        return names_x_columns[column_name]
    return names_x_columns[column_name].desc()
