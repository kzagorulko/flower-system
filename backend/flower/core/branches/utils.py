from .models import BranchModel, UserBranchModel


class BranchNotExist(ValueError):
    pass


class BranchOfUserNotExist(ValueError):
    pass


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


async def get_by_address(data):
    if 'branch' in data:
        branch = await BranchModel.query.where(
            (BranchModel.address == data['branch'])
        ).gino.first()
        if not branch:
            raise BranchNotExist
        return branch.id
    return None
