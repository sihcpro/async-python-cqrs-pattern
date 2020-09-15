from sqlalchemy.dialects.postgresql import UUID

from base import TrackingModel, db

from ..cfg import config

SCHEMA_NAME = config.SCHEMA_NAME


class TemplateModel(TrackingModel):
    __table_args__ = dict(schema=SCHEMA_NAME)

    _id = db.Column(UUID, primary_key=True)
