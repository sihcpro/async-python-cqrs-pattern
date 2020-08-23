from .identifier import UUID, UUID_TYPE


def to_uuid(value):
    if isinstance(value, UUID_TYPE):
        return value
    return UUID(value)
