from . import regex


def email(value):
    if regex.EMAIL.match(value):
        return True, value
    return False, f"{value} is not an email address"


def phone_number(value):
    if regex.PHONE_NUMBER.match(value):
        return True, value
    return False, f"{value} is not a phone number"
