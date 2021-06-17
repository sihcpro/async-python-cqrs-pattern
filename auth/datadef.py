from datetime import datetime, timedelta
from functools import partial
from pyrsistent import field

from base import factory, hashes, validator, variant
from base.data import PayloadData
from base.identifier import UUID_GENR, UUID_TYPE
from base.type import nullable
from .cfg import config


class DeviceData(PayloadData):
    device = field(str, mandatory=True)
    location = field(nullable(str))
    information = field(nullable(str))


class LoginData(DeviceData):
    username = field(str, mandatory=True)
    password = field(str, mandatory=True, factory=lambda x: str(x))


class ResetPasswordRequest(PayloadData):
    email = field(str, mandatory=True)


class ResetPasswordConfirm(DeviceData):
    email = field(str, mandatory=True)
    code = field(str, mandatory=True)


class ResetPasswordRequestData(PayloadData):
    _id = field(UUID_TYPE, mandatory=True, initial=UUID_GENR)
    user_id = field(UUID_TYPE, mandatory=True, factory=factory.to_uuid)

    request_type = field(str, mandatory=True)
    code = field(str, mandatory=True)
    expiration_date = field(
        datetime, mandatory=True, initial=lambda: datetime.utcnow() + timedelta(days=3)
    )

    _created = field(datetime, mandatory=True, initial=datetime.utcnow)
    _updated = field(datetime, mandatory=True, initial=datetime.utcnow)
    _etag = field(str, mandatory=True, initial=hashes.generate_v1)


class ChangePasswordData(PayloadData):
    current_password = field(str, mandatory=True, factory=lambda x: str(x))
    new_password = field(str, mandatory=True, factory=lambda x: str(x))


class AuthUserData(DeviceData):
    _id = field(UUID_TYPE, mandatory=True, initial=UUID_GENR)
    user_id = field(UUID_TYPE, mandatory=True, factory=factory.to_uuid)
    auth_key = field(
        str, mandatory=True, initial=partial(hashes.generate, config.AUTH_KEY_LENGTH)
    )

    _created = field(datetime, mandatory=True, initial=datetime.utcnow)
    _updated = field(datetime, mandatory=True, initial=datetime.utcnow)
    _etag = field(str, mandatory=True, initial=hashes.generate_v1)


class UserData(PayloadData):
    _id = field(UUID_TYPE, factory=factory.to_uuid, mandatory=True, initial=UUID_GENR)

    is_activate = field(bool, mandatory=True, initial=True)
    status = field(int, mandatory=True, initial=0)

    is_verified__phone = field(bool, initial=False, mandatory=True)
    is_verified__email = field(bool, initial=False, mandatory=True)

    username = field(str, mandatory=True, invariant=variant.min_length(4, "username"))
    password = field(str, mandatory=True, invariant=variant.min_length(8, "password"))

    fullname = field(str, mandatory=True)
    email = field(nullable(str))

    gender = field(nullable(int))
    year_of_birth = field(nullable(int))

    contact__phone = field(nullable(str))
    contact__email = field(str, mandatory=True, invariant=validator.email)

    address__city = field(nullable(str))
    address__district = field(nullable(str))
    address__address = field(nullable(str))
    address__zipcode = field(nullable(str))

    is_searchable = field(bool, mandatory=True, initial=True)
    notify_new_post = field(bool, mandatory=True, initial=True)
    notify_reminder = field(bool, mandatory=True, initial=True)
    _etag = field(str)


class UserInfo(UserData):
    auth_key = field(str)
    device = field(str, mandatory=True)
    location = field(nullable(str))
    information = field(nullable(str), factory=lambda x: str(x))
