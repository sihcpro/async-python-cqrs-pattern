from sqlalchemy.dialects.postgresql import UUID

from base import TrackingModel, Model, db

from .cfg import config


class UserModel(TrackingModel):
    __table_args__ = dict(schema=config.SCHEMA_NAME, extend_existing=True)
    __tablename__ = "user"

    _id = db.Column(UUID, primary_key=True)
    is_activate = db.Column(db.Boolean())
    status = db.Column(db.Integer())

    username = db.Column(db.String(255))
    password = db.Column(db.String(1023))

    name__given = db.Column(db.String(255))
    name__family = db.Column(db.String(255))

    gender = db.Column(db.Integer())
    date_of_birth = db.Column(db.DateTime(timezone=False))
    year_of_birth = db.Column(db.Integer())

    contact__phone = db.Column(db.String(15))
    contact__email = db.Column(db.String(255))

    is_verified__phone = db.Column(db.Boolean())
    is_verified__email = db.Column(db.Boolean())

    address__city = db.Column(db.String(31))
    address__district = db.Column(db.String(31))
    address__address = db.Column(db.String(255))
    address__zipcode = db.Column(db.String(31))


class UserAuthModel(Model):
    __table_args__ = dict(schema=config.SCHEMA_NAME)
    __tablename__ = "user-auth"

    _id = db.Column(UUID, primary_key=True)
    user_id = db.Column(
        UUID, db.ForeignKey(f'{config.get_module_config("app").SCHEMA_NAME}.user._id'),
    )

    auth_key = db.Column(db.String(255))
    device = db.Column(db.String(63))
    location = db.Column(db.String(255))
    information = db.Column(db.String(511))

    _created = db.Column(db.DateTime(timezone=False))