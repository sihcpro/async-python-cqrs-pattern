from gino.ext.sanic import Gino

db = Gino()


class Model(db.Model):
    _created = db.Column(db.DateTime(timezone=False))


__all__ = ("db", "Model")
