import os
from .config import MEDIA_FOLDER
if not os.path.exists(MEDIA_FOLDER):
    os.mkdir(MEDIA_FOLDER)

from .config import DB_URL
from .core.database import db
from .application import create_app

__all__ = ['create_app', 'DB_URL', 'db']
