from typing import Any, BinaryIO
from sanic.request import File

from base import hashes
from base.helper.file import get_file_name, get_valid_file_path

from ..cfg import logger
from .s3_base import S3Base


class S3Upload(S3Base):
    def __get_file_info(self, _file: Any) -> (str, str):
        """
            return file and filename
        """

        if isinstance(_file, str):
            return get_valid_file_path(_file), get_file_name(_file)
        elif isinstance(_file, File):
            filedata, filename = _file[1], _file[2]
            self.init_tmp_file(filename)
            self.tmp_file.write(filedata)
            self.tmp_file.close()
            return self.tmp_file.name, get_file_name(self.tmp_file.name)
        elif isinstance(_file, BinaryIO):
            return _file.name, get_file_name(_file.name)
        else:
            raise TypeError(f"Can't upload type {type(_file)}")

    async def upload(
        self,
        _file: Any,
        new_filename: str = None,
        public=False,
        content_type="text/plain",
    ) -> str:
        """
            _file can be directory, Sanic File, or python file open in binary
        """
        file_path, filename = self.__get_file_info(_file)

        args = {"ContentType": content_type}
        if public:
            args["ACL"] = "public-read"
        logger.debug(
            "<~~~~~~~ Upload '%s' type %s"
            % (
                filename
                if new_filename is None
                else f"{filename}' -> '{new_filename}",
                type(_file),
            )
        )
        data = dict(
            Filename=file_path,
            Bucket=self.bucket_name,
            Key=new_filename or filename,
            ExtraArgs=args,
        )
        self.response = self.client.upload_file(**data)
        self.set_object(data)

        return self.object_info

    async def upload_with_hash_name(self, _file: Any) -> str:
        new_name = hashes.generate_v1()
        file_str, filename = self.__get_file_info(_file)

        return
