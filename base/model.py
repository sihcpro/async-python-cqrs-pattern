from gino.ext.sanic import Gino

db = Gino()
Model = db.Model


__all__ = ("db", "Model")
