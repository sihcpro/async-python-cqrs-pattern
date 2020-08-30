from .s3_download import S3Download
from .s3_upload import S3Upload


class EasyS3(S3Download, S3Upload):
    pass
