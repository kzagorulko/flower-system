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

REFRESH_TOKEN_EXPIRES = datetime.timedelta(
    days=int(config('REFRESH_TOKEN_EXPIRES'))
) if int(config('REFRESH_TOKEN_EXPIRES')) else False

ACCESS_TOKEN_EXPIRES = datetime.timedelta(
    minutes=int(config('ACCESS_TOKEN_EXPIRES'))
) if int(config('ACCESS_TOKEN_EXPIRES')) else False

SECRET_KEY = config('SECRET_KEY')
JWT_ALGORITHM = config('JWT_ALGORITHM')
