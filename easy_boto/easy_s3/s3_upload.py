from typing import Any, BinaryIO
from sanic.request import File

from base.helper.file import get_file_name, get_valid_file_path

from ..cfg import logger
from .s3_base import S3Base


class S3Upload(S3Base):
    def upload(self, _file: Any) -> str:
        logger.debug(
            f"<~~~~~~~ Upload {_file[2] if isinstance(_file, File) else str(_file) }"
        )
        if isinstance(_file, str):
            self.response = self.client.upload_file(
                get_valid_file_path(_file), self.bucket_name, get_file_name(_file)
            )
        elif isinstance(_file, File):
            self.response = self.client.upload_file(
                _file[1], self.bucket_name, _file[2]
            )
        elif isinstance(_file, BinaryIO):
            self.response = self.client.upload_file(_file, self.bucket_name, _file.name)
        else:
            raise TypeError(f"Can't upload type {type(_file)}")

        return self.response
