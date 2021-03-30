from pyrsistent import field

from core.command import RootCommand
from core.define import Command, Context, Proxy
from easy_boto import EasyS3
from ....cfg import config
from ..datadef.file import UploadFileData, UploadFileEventData
from ..domain import BaseDomain


@BaseDomain.register_entity
class UploadFile(RootCommand):
    data = field(UploadFileData, mandatory=True)


@BaseDomain.command_handler(UploadFile)
async def handle__create_file(proxy: Proxy, context: Context, cmd: Command):
    s3_file = EasyS3(config.FILE_BUCKET)

    for _file in cmd.data.files:
        s3_file.upload(_file)
    data = UploadFileEventData.extend_pclass(
        cmd.data, identifier=context.initiator.identifier
    )

    yield proxy.create_event(
        "file-created",
        data,
        {"resource": "file", "identifier": context.initiator.identifier},
    )
    yield proxy.create_response("generic-file-response", {"_id": data._id})
