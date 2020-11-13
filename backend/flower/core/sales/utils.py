import os

from uuid import uuid4
from ...config import MEDIA_FOLDER


class MediaUtils:
    """
    Uses starlette 'UploadFile'
    """
    @staticmethod
    async def save_file(ext_file, _path=None):
        f_type, ext = ext_file.content_type.split('/')
        file_name = str(uuid4()) + '.' + ext

        path = file_name[:2]
        if _path is not None:
            os.remove(_path)

        if not os.path.exists(os.path.join(MEDIA_FOLDER, path)):
            os.makedirs(os.path.join(MEDIA_FOLDER, path))

        path = os.path.join(path, file_name[2:])

        with open(os.path.join(MEDIA_FOLDER, path), 'wb') as fh:
            fh.write(await ext_file.read())

        return path

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
