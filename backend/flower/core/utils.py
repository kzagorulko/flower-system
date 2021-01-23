import os
import jwt
import datetime

from pytz import utc
from uuid import uuid4
from functools import wraps
from base64 import b64decode
from mimetypes import guess_extension
from calendar import monthrange
from starlette.requests import Request
from starlette.responses import JSONResponse, Response


from .. import config
from .database import db
from .models import (
    UserModel, RoleModel, PermissionModel, PermissionAction,
)


async def _extract_user(headers, token_type):
    if 'authorization' not in headers:
        raise UserExtractionError(
            description='Missing Authentication Token',
            status_code=401
        )

    token = headers['authorization'].split(' ')[1]

    payload = jwt.decode(
        token, config.SECRET_KEY, algorithms=[config.JWT_ALGORITHM]
    )

    if (
            'iat' not in payload or 'session' not in payload
            or 'token_type' not in payload
            or payload['token_type'] != token_type
    ):
        raise UserExtractionError(
            description='Invalid auth token',
            status_code=400
        )

    user = await UserModel.query.where(
        UserModel.session == payload['session']
    ).gino.first()

    if not user:
        raise UserExtractionError(
            description='User not found or token was revoked',
            status_code=404
        )

    return user


def jwt_required(*arguments, return_user=True, token_type='access'):
    def wrapper(func):
        async def wrapper_view(*args, **kwargs):
            request = list(
                filter(lambda arg: isinstance(arg, Request), args)
            )[0]

            if not hasattr(request, 'headers'):
                return make_error('Missing headers', status_code=400)
            headers = request.headers

            try:
                user = await _extract_user(headers, token_type)
            except UserExtractionError as e:
                return make_error(e.description, status_code=e.status_code)
            except jwt.exceptions.ExpiredSignatureError:
                return make_error('Signature has expired', status_code=401)
            except jwt.exceptions.DecodeError:
                return make_error('Token is corrupted', status_code=400)

            if return_user:
                return await func(*args, user=user, **kwargs)
            return await func(*args, **kwargs)

        return wrapper_view

    if len(arguments) > 0:
        return wrapper(arguments[0])
    return wrapper


class Permissions:
    actions = PermissionAction

    def __init__(self, app_name):
        self.app_name = app_name

    def required(
            self, action, additional_actions=(), *arguments,
            return_role=False, return_user=False, return_actions=False
    ):
        def wrapper(func):
            async def wrapper_view(*args, user, **kwargs):
                if not user:
                    raise ValueError('User not in arguments!!!')
                role = await RoleModel.get(user.role_id)
                if not role:
                    return make_error(
                        "User doesn't have a role", status_code=403
                    )
                actions_clause = (PermissionModel.action == action)
                for additional_action in additional_actions:
                    actions_clause |= (
                            PermissionModel.action == additional_action
                    )

                permissions = await PermissionModel.query.where(
                    (PermissionModel.app_name == self.app_name)
                    & actions_clause
                    & (PermissionModel.role_id == role.id)
                ).gino.all()

                if not permissions:
                    return make_error(
                        "Forbidden", status_code=403
                    )

                actions = [permission.action for permission in permissions]

                return_values = {
                    'actions': (return_actions, actions),
                    'user': (return_user, user),
                    'role': (return_role, role),
                }

                results = self.get_results(return_values)

                return await func(*args, **results, **kwargs)

            return wrapper_view

        if len(arguments) > 0:
            return wrapper(arguments[0])
        return wrapper

    async def get_actions(self, role_id):
        actions = await db.select([
            PermissionModel.action
        ]).select_from(
            PermissionModel
        ).where(
            (PermissionModel.app_name == self.app_name)
            & (PermissionModel.role_id == role_id)
        ).gino.all()
        return {
            'actions': [action[0] for action in actions]
        }

    @staticmethod
    def get_results(return_values):
        results = {}
        for key, value in return_values.items():
            if value[0]:
                results[key] = value[1]

        return results


async def is_user_in_branch(user, branch) -> bool:
    return user.branch_id == branch.id


async def is_user_role_in(user, role_names) -> bool:
    roles = await RoleModel.query.where(
        RoleModel.name.in_(role_names)
    ).gino.all()

    for role in roles:
        if user.role_id == role.id:
            return True
    return False


class MediaUtils:
    @staticmethod
    async def save_file_base64(ext_file):
        service_data, base64_data = ext_file.split(',')
        ext = guess_extension(service_data.split(';')[0].split(':')[-1])

        file_name = MediaUtils.create_filename(ext)

        path = file_name[:2]

        MediaUtils.create_folder_if_not_exist(
            os.path.join(config.MEDIA_FOLDER, path)
        )

        path = os.path.join(path, file_name[2:])

        with open(os.path.join(config.MEDIA_FOLDER, path), 'wb') as fh:
            fh.write(b64decode(base64_data))

        return path

    @staticmethod
    def create_folder_if_not_exist(path):
        if not os.path.exists(path):
            os.makedirs(path)

    @staticmethod
    def create_filename(ext):
        return str(uuid4()) + ext

    @staticmethod
    def delete_file(path):
        full_path = MediaUtils.generate_full_path(path)

        try:
            os.remove(full_path)

            dir_path = os.path.split(full_path)[0]

            if not os.listdir(dir_path):
                os.rmdir(dir_path)
        except FileNotFoundError:
            pass

    @staticmethod
    def generate_full_path(path):
        # PS: normpath на Windows преобразует обычные слеши в обратные
        return os.path.normpath(os.path.join(config.MEDIA_FOLDER, path))


def convert_to_utc(dt):
    """Return same datetime if it's aware or sets it's timezone to UTC."""

    if dt is None:
        dt = datetime.datetime.utcfromtimestamp(0)

    if dt.tzinfo is None or dt.tzinfo.utcoffset(dt) is None:
        return dt.replace(tzinfo=utc)

    return dt


class GinoQueryHelper:
    LTE = '<='
    GTE = '>='

    @staticmethod
    def pagination(query_params, current_query):
        if 'page' in query_params and 'perPage' in query_params:
            page = int(query_params['page']) - 1
            per_page = int(query_params['perPage'])
            return current_query.limit(per_page).offset(page * per_page)
        return current_query

    """
    columns_map = {
       "column_name": Model.column,
    }
    """
    @staticmethod
    def order(query_params, current_query, columns_map):
        def _get_column(column_name, asc=True):
            if asc:
                return columns_map[column_name]
            return columns_map[column_name].desc()

        if 'order' in query_params and 'field' in query_params:
            return current_query.order_by(
                _get_column(
                    query_params['field'],
                    query_params['order'] == 'ASC'
                )
            )

        return current_query

    @staticmethod
    def search(field, value, current_query, total_query):
        return (
            current_query.where(field.ilike(f'%{value}%')),
            total_query.where(field.ilike(f'%{value}%'))
        )

    @staticmethod
    def equal(field, value, current_query, total_query):
        return (
            current_query.where(field == value),
            total_query.where(field == value)
        )

    @staticmethod
    def in_(current_query, total_query, field, values):
        return (
            current_query.where(field.in_(values)),
            total_query.where(field.in_(values))
        )

    @staticmethod
    def month_year_cond(field, value, c_type, current_query, total_query):
        custom_date = GinoQueryHelper.prepare_custom_date(value, c_type)

        if c_type == GinoQueryHelper.LTE:
            return (
                current_query.where(field <= custom_date),
                total_query.where(field <= custom_date)
            )
        else:
            return (
                current_query.where(field >= custom_date),
                total_query.where(field >= custom_date)
            )

    @staticmethod
    def prepare_custom_date(date_str, c_type=None):
        date_list = date_str.split('-')

        year = int(date_list[0])
        month = int(date_list[1])

        if len(date_list) > 2:
            day = int(date_list[2])
        elif not c_type or c_type == GinoQueryHelper.GTE:
            day = 1
        else:
            day = monthrange(year, month)[1]

        return datetime.date(year, month, day)


def make_error(description, status_code=400):
    return JSONResponse({
        'description': description
    }, status_code=status_code)


def with_transaction(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        connection = args[1].get('connection')

        # Offline mode
        if not connection:
            print('Warning! Offline mode!')
            return await func(*args, **kwargs)

        tx = await connection.transaction()

        try:
            result = await func(*args, **kwargs)

            # Workaround for an inability to move `serializer_middleware` to
            # the start of middlewares: attempt to get status and
            # response from result as tuple or standalone object.
            status = 200
            commit_anyway = False

            if isinstance(result, tuple) and len(result) > 1:
                status = result[1]
            elif isinstance(result, Response):
                status = result.status_code
                if hasattr(result, 'commit_anyway'):
                    commit_anyway = result.commit_anyway

            if commit_anyway or (199 < status < 400):
                await tx.commit()
            else:
                await tx.rollback()
            return result
        except Exception:
            await tx.rollback()
            raise
    return wrapper


class TokenTypeError(TypeError):
    pass


class UserExtractionError(Exception):
    def __init__(self, description, status_code, *args):
        super().__init__(*args)
        self.description = description
        self.status_code = status_code


class ParamsMissingError(Exception):
    pass


def _encode_jwt(session, token_type):
    algorithm = config.JWT_ALGORITHM
    time_now = datetime.datetime.utcnow()

    header = {'class': token_type}
    payload = {
        'iat': time_now,
        'session': session,
        'token_type': token_type,
    }

    if token_type == 'refresh':
        if isinstance(config.REFRESH_TOKEN_EXPIRES, datetime.timedelta):
            payload['exp'] = time_now + config.REFRESH_TOKEN_EXPIRES
    elif token_type == 'access':
        if isinstance(config.ACCESS_TOKEN_EXPIRES, datetime.timedelta):
            payload['exp'] = time_now + config.ACCESS_TOKEN_EXPIRES
    else:
        raise TokenTypeError

    return jwt.encode(
        payload, config.SECRET_KEY, algorithm, header
    ).decode('utf-8')


def create_access_token(session):
    return _encode_jwt(session, 'access')


def create_refresh_token(session):
    return _encode_jwt(session, 'refresh')


def make_list_response(items, total):
    return JSONResponse({
        'items': items,
        'total': total,
    })


def make_response(content, background=None):
    if background:
        return JSONResponse(content, background=background)
    return JSONResponse(content)


def check_missing_params(query, data):
    errors = []

    for param_key in data:
        if param_key not in query:
            errors.append(f"Parameter `{param_key}` required")

    if errors:
        raise ParamsMissingError("\n".join(errors), 400)


NO_CONTENT = Response('', status_code=204)
