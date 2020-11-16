from ..models import ProviderModel


async def is_name_unique(name):
    provider = await ProviderModel.query.where(
        ProviderModel.name == name
    ).gino.first()
    if provider:
        return False
    return True
