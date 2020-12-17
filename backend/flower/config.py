import datetime

from starlette.config import Config
from sqlalchemy.engine.url import URL


config = Config('.env')

DB_HOST = config('DB_HOST')
DB_PORT = config('DB_PORT')
DB_USER = config('DB_USER')
DB_PASSWORD = config('DB_PASSWORD')
DB_DATABASE = config('DB_DATABASE')

DB_URL = URL(
    drivername='postgres',
    host=DB_HOST,
    port=DB_PORT,
    username=DB_USER,
    password=DB_PASSWORD,
    database=DB_DATABASE
)


def _cast_token_expires(value, unit='days'):
    try:
        return datetime.timedelta(**{unit: config(value, cast=int)})
    except ValueError:
        pass
    try:
        return config(value, cast=bool)
    except ValueError:
        raise ValueError(f'{config(value)} is not int or bool value')


SERVER_HOST = config('SERVER_HOST')
SERVER_PORT = config('SERVER_PORT')
SERVER_PROTOCOL = config('SERVER_PROTOCOL')
SERVER_HOSTNAME = (
    SERVER_PROTOCOL + "://" + SERVER_HOST + ":" + SERVER_PORT + "/"
)

REFRESH_TOKEN_EXPIRES = _cast_token_expires('REFRESH_TOKEN_EXPIRES', 'days')
ACCESS_TOKEN_EXPIRES = _cast_token_expires('ACCESS_TOKEN_EXPIRES', 'minutes')

SECRET_KEY = config('SECRET_KEY')
JWT_ALGORITHM = config('JWT_ALGORITHM')

ADMIN_USERNAME = config('ADMIN_USERNAME')
ADMIN_PASSWORD = config('ADMIN_PASSWORD')
ADMIN_DISPLAY_NAME = config('ADMIN_DISPLAY_NAME')
ADMIN_EMAIL = config('ADMIN_EMAIL')

MEDIA_FOLDER = config('MEDIA_FOLDER')

TESTING = config('TESTING', cast=bool, default=False)

if TESTING:
    DB_USER = 'flower_test_user'
    DB_PASSWORD = 'flower_test_user'
    DB_DATABASE = 'flower_test'

    DB_URL = URL(
        drivername='postgres',
        host=DB_HOST,
        port=DB_PORT,
        username=DB_USER,
        password=DB_PASSWORD,
        database=DB_DATABASE
    )
