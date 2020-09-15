from sqlalchemy.dialects.postgresql import UUID

from base import Model

from .template import SCHEMA_NAME, db


class FileModel(Model):
    __table_args__ = dict(schema=SCHEMA_NAME, extend_existing=True)
    __tablename__ = "files"

    _id = db.Column(UUID, primary_key=True)
    user_id = db.Column(UUID)

    bucket_name = db.Column(db.String(127))
    filename = db.Column(db.String(127))
    description = db.Column(db.String(255))
