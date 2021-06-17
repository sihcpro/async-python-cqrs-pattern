import sqlalchemy
from datetime import datetime
from gino import Gino

from .hashes import generate_v1

db: sqlalchemy = Gino()


class Model(db.Model):
    _created = db.Column(db.DateTime(timezone=False), default=datetime.utcnow)
    _updated = db.Column(db.DateTime(timezone=False), default=datetime.utcnow)

    _etag = db.Column(db.String(255), default=generate_v1)


__all__ = ("db", "Model")
