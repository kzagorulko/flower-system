import os
import base64

from uuid import uuid4
from ...config import MEDIA_FOLDER


class MediaUtils:
    """
    Uses starlette 'UploadFile'
    """
    @staticmethod
    async def save_file(ext_file, _path=None):
        f_type, ext = ext_file.content_type.split('/')
        file_name = MediaUtils.create_filename(ext)

        path = file_name[:2]
        if _path is not None:
            os.remove(_path)

        MediaUtils.create_folder_if_not_exist(
            os.path.join(MEDIA_FOLDER, path)
        )

        path = os.path.join(path, file_name[2:])

        with open(os.path.join(MEDIA_FOLDER, path), 'wb') as fh:
            fh.write(await ext_file.read())

        return path

    @staticmethod
    async def save_file_base64(ext_file, _path=None):
        service_data, base64_data = ext_file.split(',')
        ext = service_data.split(';')[0][5:].split('/')[1]

        file_name = MediaUtils.create_filename(ext)

        path = file_name[:2]
        if _path is not None:
            os.remove(_path)

        MediaUtils.create_folder_if_not_exist(
            os.path.join(MEDIA_FOLDER, path)
        )

        path = os.path.join(path, file_name[2:])
        print(base64.b64decode(base64_data))
        with open(os.path.join(MEDIA_FOLDER, path), 'wb') as fh:
            fh.write(base64.b64decode(base64_data))

        return path

    @staticmethod
    def create_folder_if_not_exist(path):
        if not os.path.exists(path):
            os.makedirs(path)

    @staticmethod
    def create_filename(ext):
        return str(uuid4()) + '.' + ext

    @staticmethod
    def del_file(path):
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
        return os.path.normpath(os.path.join(MEDIA_FOLDER, path))
