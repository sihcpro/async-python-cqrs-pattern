from pyrsistent import field

from base import TrackingModel, TrackingPayloadData, UUID_TYPE, PayloadData, Model


class BaseResource:
    __resource_name__ = "resource-name"
    __backend__ = Model


class Resource(BaseResource, PayloadData):
    _id = field(UUID_TYPE, mandatory=True)


class TrackingResource(BaseResource, TrackingPayloadData):
    __backend__ = TrackingModel

    _id = field(UUID_TYPE, mandatory=True)
