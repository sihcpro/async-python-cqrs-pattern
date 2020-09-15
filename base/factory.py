from datetime import datetime

from .cfg import config
from .identifier import UUID, UUID_TYPE


def to_uuid(value) -> UUID_TYPE:
    if isinstance(value, UUID_TYPE):
        return value
    return UUID(value)


def to_datetime(value, date_fmt=config.DATETIME_FORMAT) -> datetime:
    if isinstance(value, datetime):
        return value
    return datetime.strptime(value, date_fmt)
