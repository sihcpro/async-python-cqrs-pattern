import random
import string

from .cfg import config


def generate_v1(_length=config.DEFAULT_GENERATE_LENGTH) -> str:
    return "".join([random.choice(string.hexdigits) for i in range(_length)])


def generate(_length=config.DEFAULT_GENERATE_LENGTH) -> str:
    return "generate_v1." + generate_v1(_length)
