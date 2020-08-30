import re
from enum import Enum


def __sif__():
    re_pascal_to_snake_case = re.compile(r"(?<!^)(?=[A-Z])")

    def _pascal_to_snake_case(name):
        return re_pascal_to_snake_case.sub("-", name).lower()

    return _pascal_to_snake_case


pascal_to_snake_case = __sif__()


def to_json_value(value):
    if value is None:
        return value
    if isinstance(value, Enum):
        return value.name
    return str(value)
