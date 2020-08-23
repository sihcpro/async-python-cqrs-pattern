from pyrsistent import field

from base import TrackingModel, TrackingPayloadData, UUID_TYPE


class Resource(TrackingPayloadData):
    __resource__ = "resource-name"
    __backend__ = TrackingModel

    _id = field(UUID_TYPE, mandatory=True)
