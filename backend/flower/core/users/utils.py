from . import UserModel
from ..models import RoleModel


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


def get_column_for_order(column_name, asc=True):
    names_x_columns = {
        'id': UserModel.id,
        'displayName': UserModel.display_name,
        'role': RoleModel.display_name,
    }

    if asc:
        return names_x_columns[column_name]
    return names_x_columns[column_name].desc()
