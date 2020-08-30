import os
import boto3
from typing import BinaryIO
from tempfile import NamedTemporaryFile

from base.helper.file import get_file_extension, get_valid_file_path

from ..cfg import config, logger
from ..helper import create_boto3_environment


class S3Base:
    def __init__(
        self,
        bucket_name,
        access_key=config.ACCESS_KEY,
        access_secret=config.ACCESS_SECRET,
        default_region=config.DEFAULT_REGION,
        exists_env=False,
    ):
        """
        exists_env: If you allready setup S3 Amazon environment then set True
        """
        logger.debug(f"~~~~~~~> Connect bucket: {bucket_name}")

        self.__bucket_name = bucket_name
        if not exists_env:
            create_boto3_environment(access_key, access_secret, default_region)

        self.__resource = boto3.resource("s3")
        self.__client = boto3.client("s3")
        self.__bucket = self.__resource.Bucket(self.__bucket_name)

        self.__tmp_file__: BinaryIO = None
        self.response = None
        self.filename = None

    def init_tmp_file(self, filename, file_path: str = None):
        self.__destroy_tmp_file()
        if self.filename == filename:
            return

        if file_path is not None:
            file_path = get_valid_file_path(
                file_path, filename, file_exist=False
            )
            self.__tmp_file__ = open(file_path, "wb+")
        else:
            self.__tmp_file__ = NamedTemporaryFile(
                suffix=f".{get_file_extension(filename)}", delete=False
            )
            self.filename = self.__tmp_file__.name

    def __destroy_tmp_file(self):
        if self.__tmp_file__ is not None:
            self.__tmp_file__.close()
            os.unlink(self.__tmp_file__.name)

    def __del__(self):
        self.__destroy_tmp_file()

    @property
    def tmp_file(self) -> BinaryIO:
        return self.__tmp_file__

    @property
    def bucket_name(self):
        return self.__bucket_name

    @property
    def client(self):
        return self.__client

    @property
    def resource(self):
        return self.__resource

    @property
    def bucket(self):
        return self.__bucket
