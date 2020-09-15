from pyrsistent import field

from core import Resource
from base import UUID_TYPE
from base.type import nullable

from ....model.file import FileModel
from ..domain import UserDomain


@UserDomain.register_resource
class FileResource(Resource):
    __resource_name__ = "file"
    __backend__ = FileModel

    _id = field(UUID_TYPE, mandatory=True)
    user_id = field(UUID_TYPE, mandatory=True)

    bucket_name = field(str, mandatory=True)
    filename = field(str, mandatory=True)
    description = field(nullable(str))
