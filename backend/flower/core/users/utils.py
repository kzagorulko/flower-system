from sqlalchemy.dialects.postgresql import insert

from ..database import db
from ..models import RoleModel, UserModel, UserBranchModel


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


async def change_branches(branches, user_id, is_create=False):
    branches = list(set(branches))
    if len(branches) == 0:
        await UserBranchModel.delete.where(
            UserBranchModel.user_id == user_id
        ).gino.status()
    else:
        branches_exist = await UserBranchModel.query.where(
            (UserBranchModel.user_id == user_id)
            & (UserBranchModel.branch_id.in_(branches))
        ).gino.all()

        count = await db.select(
            [db.func.count(UserBranchModel.branch_id)]
        ).where(
            UserBranchModel.user_id == user_id
        ).gino.scalar()

        if len(branches_exist) != len(branches) or count != len(branches):
            if not is_create:
                await UserBranchModel.delete.where(
                    (UserBranchModel.user_id == user_id) &
                    ~ (UserBranchModel.branch_id.in_(branches))
                ).gino.status()

            models_ids = [model.branch_id for model in branches_exist]

            result = []

            for branch in branches:
                if branch not in models_ids:
                    result.append({'user_id': user_id, 'branch_id': branch})

            if result:
                await insert(UserBranchModel.__table__).values(
                    result
                ).on_conflict_do_nothing().gino.scalar()
