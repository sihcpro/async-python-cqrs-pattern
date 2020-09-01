import os
import boto3
from typing import BinaryIO
from tempfile import NamedTemporaryFile

from base.helper.file import get_file_extension, get_valid_file_path

from ..cfg import config, logger
from ..helper import create_boto3_environment, get_s3_url


class S3Base:
    __is_connected = False
    __resource = None
    __client = None

    @classmethod
    def connect(
        cls,
        access_key=config.ACCESS_KEY,
        access_secret=config.ACCESS_SECRET,
        default_region=config.DEFAULT_REGION,
        exists_env=False,
    ):
        """
        exists_env: If you allready setup S3 Amazon environment then set True
        """
        if cls.__is_connected:
            return

        logger.debug("~~~~~~~> Connect to S3 Amazon")
        if not exists_env:
            create_boto3_environment(access_key, access_secret, default_region)

        cls.__resource = boto3.resource("s3")
        cls.__client = boto3.client("s3")
        cls.__region = default_region
        cls.__is_connected = True

    def __init__(
        self, bucket_name,
    ):
        if not self.__is_connected:
            self.connect()

        logger.debug(f"~~~~~~~> Connect bucket: {bucket_name}")

        self.__bucket_name = bucket_name
        self.__bucket = self.__resource.Bucket(self.__bucket_name)

        self.__tmp_file__: BinaryIO = None
        self.response = None
        self.__filename = None
        self.__object: dict = None

    def init_tmp_file(self, filename, file_path: str = None):
        self.__destroy_tmp_file()
        if self.__filename == filename:
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
            self.__filename = self.__tmp_file__.name

    def __destroy_tmp_file(self):
        if self.__tmp_file__ is not None:
            self.__tmp_file__.close()
            os.unlink(self.__tmp_file__.name)

    def __del__(self):
        self.__destroy_tmp_file()

    def set_object(self, data: dict):
        self.__object = data
        self.__object["Url"] = get_s3_url(self)

    def update_object(self, data: dict, **args):
        if data:
            self.__object.update(data)
        self.__object.update(args)

    @property
    def object_info(self) -> dict:
        return self.__object

    @property
    def tmp_file(self) -> BinaryIO:
        return self.__tmp_file__

    @property
    def filename(self):
        return self.__filename

    @property
    def region(self):
        return self.__region

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
