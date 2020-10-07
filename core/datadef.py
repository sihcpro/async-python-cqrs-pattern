from pyrsistent import field

from base import factory, PayloadData, UUID_GENR, UUID_TYPE


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
