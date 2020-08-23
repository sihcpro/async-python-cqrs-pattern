import uuid

UUID_TYPE = uuid.UUID


def UUID_GENR() -> UUID_TYPE:
    return uuid.uuid4()


def UUID(value) -> UUID_TYPE:
    return UUID_TYPE(value)
