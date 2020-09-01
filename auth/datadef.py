from datetime import datetime
from functools import partial
from pyrsistent import field

from base import factory, hashes, validator, variant
from base.data import PayloadData
from base.identifier import UUID_GENR, UUID_TYPE
from base.type import nullable

from .cfg import config


class LoginData(PayloadData):
    username = field(str, mandatory=True)
    password = field(str, mandatory=True, factory=lambda x: str(x))

    device = field(str, mandatory=True)
    location = field(nullable(str))
    information = field(nullable(str), factory=lambda x: str(x))


class AuthUserData(PayloadData):
    _id = field(UUID_TYPE, mandatory=True, initial=UUID_GENR)
    user_id = field(UUID_TYPE, mandatory=True, factory=factory.to_uuid)
    auth_key = field(
        str, mandatory=True, initial=partial(hashes.generate, config.AUTH_KEY_LENGTH)
    )

    device = field(str, mandatory=True)
    location = field(nullable(str))
    information = field(nullable(str))

    _created = field(datetime, mandatory=True, initial=datetime.utcnow)


class UserInfo(PayloadData):
    _id = field(UUID_TYPE, mandatory=True)

    fullname = field(str, mandatory=True)

    email = field(nullable(str))

    gender = field(nullable(int))
    year_of_birth = field(nullable(int))


class UserData(PayloadData):
    _id = field(UUID_TYPE, mandatory=True, initial=UUID_GENR)

    is_activate = field(bool, mandatory=True, initial=True)
    status = field(int, mandatory=True, initial=0)

    is_verified__phone = field(bool, initial=False, mandatory=False)
    is_verified__email = field(bool, initial=False, mandatory=False)

    username = field(str, mandatory=True, invariant=variant.min_length(4, "username"))
    password = field(str, mandatory=True, invariant=variant.min_length(8, "password"))

    fullname = field(str, mandatory=True)

    contact__phone = field(nullable(str))
    contact__email = field(str, mandatory=True, invariant=validator.email)

    address__city = field(nullable(str))
    address__district = field(nullable(str))
    address__address = field(nullable(str))
    address__zipcode = field(nullable(str))


class RegisterUserData(UserData):
    device = field(str, mandatory=True)
    location = field(nullable(str))
    information = field(nullable(str), factory=lambda x: str(x))
