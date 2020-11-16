import os
import datetime

from pytz import utc
from uuid import uuid4
from base64 import b64decode

from .. import config


class MediaUtils:
    @staticmethod
    async def save_file_base64(ext_file):
        service_data, base64_data = ext_file.split(',')
        ext = service_data.split(';')[0].split('/')[-1]

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
        return str(uuid4()) + '.' + ext

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
