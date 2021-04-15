from sqlalchemy.dialects.postgresql import ARRAY, UUID

from base import Model, TrackingModel, db
from .cfg import config


class UserModel(TrackingModel):
    __table_args__ = dict(schema=config.SCHEMA_NAME, extend_existing=True)
    __tablename__ = "user"

    _id = db.Column(UUID, primary_key=True)
    is_activate = db.Column(db.Boolean())
    status = db.Column(db.Integer())

    username = db.Column(db.String(255))
    password = db.Column(db.String(1023))

    fullname = db.Column(db.String(255))

    gender = db.Column(db.Integer())
    year_of_birth = db.Column(db.Integer())

    contact__phone = db.Column(db.String(15))
    contact__email = db.Column(db.String(255))

    is_verified__phone = db.Column(db.Boolean())
    is_verified__email = db.Column(db.Boolean())

    followers = db.Column(ARRAY(UUID))
    _etag = db.Column(db.String(255))


class UserAuthModel(Model):
    __table_args__ = dict(schema=config.SCHEMA_NAME)
    __tablename__ = "user-auth"

    _id = db.Column(UUID, primary_key=True)
    user_id = db.Column(
        UUID,
        db.ForeignKey(f'{config.get_module_config("app").SCHEMA_NAME}.user._id'),
    )

    auth_key = db.Column(db.String(255))
    device = db.Column(db.String(63))
    location = db.Column(db.String(255))
    information = db.Column(db.String(511))

    _created = db.Column(db.DateTime(timezone=False))
