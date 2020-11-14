from .models import BranchModel


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
