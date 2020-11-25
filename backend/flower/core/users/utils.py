from ..models import RoleModel, UserModel


class RoleNotExist(ValueError):
    pass


async def is_username_unique(username):
    user = await UserModel.query.where(
        UserModel.username == username
    ).gino.first()
    if user:
        return False
    return True


async def get_role_id(data):
    if 'role' in data:
        role = await RoleModel.query.where(
            (RoleModel.name == data['role'])
            | (RoleModel.display_name == data['role'])
        ).gino.first()
        if not role:
            raise RoleNotExist
        return role.id
    return None
