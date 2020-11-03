import jwt
import datetime

from functools import wraps
from starlette.requests import Request
from starlette.responses import Response, JSONResponse

from .. import config
from .models import UserModel


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


def jwt_required(*arguments, return_user=False, token_type='access'):
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


def create_access_token(session):
    return _encode_jwt(session, 'access')


def create_refresh_token(session):
    return _encode_jwt(session, 'refresh')


def make_error(description, status_code=400):
    return JSONResponse({
        'description': description
    }, status_code=status_code)
