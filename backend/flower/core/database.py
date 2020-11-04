from gino_starlette import Gino
from ..config import DB_HOST, DB_USER, DB_DATABASE, DB_PASSWORD, DB_PORT


db = Gino(
    driver='postgres',
    host=DB_HOST,
    port=DB_PORT,
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB_DATABASE
)
