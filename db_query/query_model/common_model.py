from .. import field
from .postgrest_model import PostgrestQueryModel


class CommonQueryModel(PostgrestQueryModel):
    _created = field.DatetimeField()
    _updated = field.DatetimeField(hidden=True)
