from sanic.response import BaseHTTPResponse, file

from ..cfg import logger
from .s3_base import S3Base


class S3Download(S3Base):
    def download(self, filename, file_path: str = None) -> str:
        self.init_tmp_file(filename, file_path)
        if self.filename == filename:
            return self.filename

        logger.debug(f"<~~~~~~~ Download '{filename}'")
        self.response = self.client.download_fileobj(
            self.bucket_name, filename, self.__tmp_file__
        )
        return self.filename

    async def response_file(self, filename) -> BaseHTTPResponse:
        if self.tmp_file is None:
            self.download(filename)

        logger.debug(f"<~~~~~~~ Response '{filename}'")
        return await (file(self.tmp_file.name, filename=filename))
