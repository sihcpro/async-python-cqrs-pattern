import re

from .cfg import config


EMAIL = re.compile(config.EMAIL_REGEX)
PHONE_NUMBER = re.compile(config.PHONE_NUMBER_REGEX)
