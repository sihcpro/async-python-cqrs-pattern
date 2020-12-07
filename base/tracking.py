from datetime import datetime
from pyrsistent import field
from sqlalchemy.dialects.postgresql import UUID

from base.type import nullable

from .data import PayloadData
from .hashes import generate_v1
from .identifier import UUID_TYPE
from .model import Model, db


class TrackingModel(Model):
    _creator = db.Column(UUID)
    _updater = db.Column(UUID)

    _deleted = db.Column(db.DateTime(timezone=False))


class TrackingPayloadData(PayloadData):
    _id = field(UUID_TYPE, mandatory=True)

    _creator = field(UUID_TYPE, mandatory=True)
    _updater = field(UUID_TYPE, mandatory=True)

    _created = field(datetime, mandatory=True)
    _updated = field(datetime, mandatory=True)
    _deleted = field(nullable(datetime))

    _etag = field(str, mandatory=True, initial=generate_v1)


def generate_tracking_data(user_id: UUID_TYPE):
    now = datetime.utcnow()
    return dict(
        _creator=user_id,
        _updater=user_id,
        _created=now,
        _updated=now,
        _etag=generate_v1(),
    )
