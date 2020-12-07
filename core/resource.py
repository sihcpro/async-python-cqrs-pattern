from datetime import datetime
from pyrsistent import field

from base import UUID_TYPE, Model, PayloadData, TrackingModel, TrackingPayloadData
from base.hashes import generate_v1
from base.type import nullable


class BaseResource:
    __resource_name__ = "resource-name"
    __model__ = Model

    @property
    def model(self) -> Model:
        return self.__model__


class Resource(BaseResource, PayloadData):
    _id = field(UUID_TYPE, mandatory=True)

    _created = field(nullable(datetime))
    _updated = field(datetime)

    _etag = field(str, mandatory=True, initial=generate_v1)


class TrackingResource(BaseResource, TrackingPayloadData):
    __model__ = TrackingModel

    _id = field(UUID_TYPE, mandatory=True)

    @property
    def model(self) -> TrackingModel:
        return self.__model__
