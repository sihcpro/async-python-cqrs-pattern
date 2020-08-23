from pyrsistent import field

from base.data import PayloadData
from base.identifier import UUID_GENR, UUID_TYPE
from base import factory


class ResourceData(PayloadData):
    resource = field(str, invariant=lambda x: (len(x) >= 4, x), mandatory=True)
    identifier = field(
        UUID_TYPE, factory=factory.to_uuid, initial=UUID_GENR, mandatory=True
    )


class Initiator(ResourceData):
    pass


class Selector(ResourceData):
    pass


class Targeter(ResourceData):
    pass
