from pyrsistent import field

from base import TrackingModel, TrackingPayloadData, UUID_TYPE, PayloadData, Model


class BaseResource:
    __resource_name__ = "resource-name"
    __model__ = Model

    @property
    def model(self) -> Model:
        return self.__model__


class Resource(BaseResource, PayloadData):
    _id = field(UUID_TYPE, mandatory=True)


class TrackingResource(BaseResource, TrackingPayloadData):
    __model__ = TrackingModel

    _id = field(UUID_TYPE, mandatory=True)

    @property
    def model(self) -> TrackingModel:
        return self.__model__
