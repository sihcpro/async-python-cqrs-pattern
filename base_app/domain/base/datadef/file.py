from pyrsistent import pvector_field, field
from sanic.request import File

from base.data import PayloadData
from base import UUID_TYPE
from base.type import nullable


class CommonFileData(PayloadData):
    files = pvector_field(File)
    description = pvector_field(str)


class UploadFileData(CommonFileData):
    pass


class UploadFileEventData(PayloadData):
    _id = field(UUID_TYPE, mandatory=True)
    user_id = field(UUID_TYPE, mandatory=True)

    bucket_name = field(str, mandatory=True)
    filename = field(str, mandatory=True)
    description = field(nullable(str))
