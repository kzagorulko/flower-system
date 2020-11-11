from ..models import RoleModel, UserModel, UserBranchModel
from sqlalchemy.dialects.postgresql import insert


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


async def change_branches(branches, user_id):
    if len(branches) == 0:
        await UserBranchModel.delete\
            .where(UserBranchModel.user_id == user_id).gino.status()
    else:
        branchesExist = await UserBranchModel.query.where(
            (UserBranchModel.user_id == user_id) &
            (UserBranchModel.branch_id in branches)
        ).gino.all()

        if len(branchesExist) != len(branches):
            await UserBranchModel.delete.where(
                ~((UserBranchModel.user_id == user_id) &
                  (UserBranchModel.branch_id in branches))
            ).gino.status()

            models_ids = [branchesExist.id for model in branchesExist]

            result = []

            for branch in branches:
                if branch not in models_ids:
                    result.append({'user_id': user_id, 'branch_id': branch})

            await insert(UserBranchModel)\
                .values(result).on_conflict_do_nothing().gino.scalar()
