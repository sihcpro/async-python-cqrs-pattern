from datetime import date, datetime

from .cfg import config
from .identifier import UUID, UUID_TYPE


def to_uuid(value) -> UUID_TYPE:
    if isinstance(value, UUID_TYPE):
        return value
    return UUID(value)


def to_date(value, date_fmt=config.DATE_FORMAT) -> date:
    if isinstance(value, date):
        return value
    return datetime.strptime(value, date_fmt).date()


def to_datetime(value, datetime_fmt=config.DATETIME_FORMAT) -> datetime:
    if isinstance(value, datetime):
        return value
    return datetime.strptime(value, datetime_fmt)


def to_int(value) -> int:
    try:
        return int(value)
    except Exception:
        return 0


def to_nulable_int(value) -> int:
    try:
        return int(value)
    except Exception:
        return None


def to_float(value) -> float:
    try:
        return float(value)
    except Exception:
        return 0


def to_nullable_float(value) -> float:
    try:
        return float(value)
    except Exception:
        return None


def __sif__():
    boolean_map = {
        "True": True,
        "False": False,
        "true": True,
        "false": False,
        "1": True,
        "0": False,
        1: True,
        0: False,
        True: True,
        False: False,
    }

    def _to_boolean(value) -> bool:
        return boolean_map.get(value, None)

    return _to_boolean


to_boolean: bool = __sif__()
