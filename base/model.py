from gino.ext.sanic import Gino

db = Gino()


class Model(db.Model):
    _created = db.Column(db.DateTime(timezone=False))
    _updated = db.Column(db.DateTime(timezone=False))

    _etag = db.Column(db.String(255))


__all__ = ("db", "Model")
