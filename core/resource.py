from datetime import datetime
from pyrsistent import field

from base import UUID_TYPE, Model, PayloadData, TrackingModel, TrackingPayloadData


class BaseResource:
    __resource_name__ = "resource-name"
    __model__ = Model

    @property
    def model(self) -> Model:
        return self.__model__


class Resource(BaseResource, PayloadData):
    _id = field(UUID_TYPE, mandatory=True)

    _created = field(datetime)


class TrackingResource(BaseResource, TrackingPayloadData):
    __model__ = TrackingModel

    _id = field(UUID_TYPE, mandatory=True)

    @property
    def model(self) -> TrackingModel:
        return self.__model__
