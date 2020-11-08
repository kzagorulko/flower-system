from ..models import BranchModel, UserModel


async def is_address_unique(address):
    branch = await BranchModel.query.where(
        BranchModel.address == address
    ).gino.first()
    if branch:
        return False
    return True


def get_column_for_order(column_name, asc=True):
    names_x_columns = {
        'id': BranchModel.id,
        'address': BranchModel.name,
    }

    if asc:
        return names_x_columns[column_name]
    return names_x_columns[column_name].desc()
