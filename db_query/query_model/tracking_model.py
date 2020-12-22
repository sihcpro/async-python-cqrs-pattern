from .. import field
from .postgrest_model import PostgrestQueryModel


class TrackingModel:
    _creator = field.DatetimeField(hidden=True)
    _updater = field.DatetimeField(hidden=True)

    _created = field.DatetimeField()
    _updated = field.DatetimeField(hidden=True)
    _deleted = field.DatetimeField(hidden=True)
    _etag = field.DatetimeField(hidden=True)


class PostgrestTrackingQueryModel(PostgrestQueryModel, TrackingModel):
    pass
