import jwt
import datetime

from functools import wraps
from starlette.responses import Response, JSONResponse

from .. import config
from ..models import UserModel


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


def _encode_jwt(identity, token_type):
    algorithm = config.JWT_ALGORITHM
    time_now = datetime.datetime.utcnow()

    header = {'class': token_type}
    payload = {
        'iat': time_now,
        'identity': identity,
        'token_type': token_type,
    }

    if token_type == 'refresh':
        if isinstance(config.REFRESH_TOKEN_EXPIRES, datetime.timedelta):
            payload['exp'] = time_now + config.REFRESH_TOKEN_EXPIRES
    elif token_type == 'access':
        if isinstance(config.ACCESS_TOKEN_EXPIRES, datetime.timedelta):
            payload['exp'] = time_now + config.ACCESS_TOKEN_EXPIRES
    else:
        print(token_type)
        raise TokenTypeError

    return jwt.encode(
        payload, config.SECRET_KEY, algorithm, header
    ).decode('utf-8')


def _jwt_verify(func, token_type='access'):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        request = args[0]
        if not hasattr(request, 'headers'):
            return make_error('Missing headers', status_code=400)
        headers = request.headers

        if 'authorization' not in headers:
            return make_error('Missing Authentication Token', status_code=401)

        token = headers['authorization'].split(' ')[1]

        try:
            payload = jwt.decode(
                token, config.SECRET_KEY, algorithms=[config.JWT_ALGORITHM]
            )
        except jwt.exceptions.ExpiredSignatureError:
            return make_error('Signature has expired', status_code=401)

        if (
                'iat' not in payload or 'identity' not in payload
                or 'token_type' not in payload
                or payload['token_type'] != token_type
        ):
            return make_error('Invalid auth token', status_code=400)

        user = await UserModel.query.where(
            UserModel.identity == payload['identity']
        ).gino.first()

        if not user:
            make_error('User not found', status_code=404)

        return await func(*args, user, **kwargs)

    return wrapper


def jwt_refresh_token_required(func):
    return _jwt_verify(func, 'refresh')


def jwt_required(func):
    return _jwt_verify(func)


def create_access_token(identity):
    return _encode_jwt(identity, 'access')


def create_refresh_token(identity):
    return _encode_jwt(identity, 'refresh')


def make_error(description, status_code=400):
    return JSONResponse({
        'description': description
    }, status_code=status_code)
