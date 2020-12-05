from typing import Tuple, Union

from base import Model
from base.identifier import UUID_TYPE

from .datadef import PayloadData, Targeter, ResourceData
from .entity import Entity
from .event import Event
from .response import BaseResponse
from .statemgr.state_manager import StateMgr
from .resource import Resource


class Proxy:
    def __init__(self, domain, statemgr: StateMgr):
        self.__domain = domain
        self.__stagemgr = statemgr

    def lookup_resource(self, resource_name: str) -> Resource:
        return self.__stagemgr.lookup_resource(resource_name)

    def lookup_model(self, resource_name: str) -> Model:
        return self.lookup_resource(resource_name).__model__

    async def fetch_target(self, target: ResourceData) -> Resource:
        return await self.__stagemgr.fetch_target(target)

    async def fetch(self, resource: str, identifier: UUID_TYPE) -> Resource:
        return await self.__stagemgr.fetch(resource, identifier)

    async def fetch_from_db(self, resource: str, identifier: UUID_TYPE) -> Resource:
        return await self.__stagemgr.fetch_from_db(resource, identifier)

    def create_response(
        self, name: str, data: PayloadData, meta: dict = None, message: str = None
    ) -> Tuple[str, BaseResponse, Entity]:
        Entity = self.__domain.lookup_entity(name)
        entity = Entity(data=data, meta=meta or {}, message=message or "OK")
        handler = self.__domain.lookup_response_handler(Entity)
        return (self.__domain.__namespace__, entity, handler)

    def create_event(
        self,
        name: str,
        data: Union[PayloadData, dict],
        targeter: Union[ResourceData, dict],
    ) -> Tuple[str, Event, Entity]:
        targeter = (
            Targeter.extend_pclass(targeter)
            if isinstance(targeter, ResourceData)
            else Targeter(**targeter)
        )

        Entity = self.__domain.lookup_entity(name)
        entity = Entity(data=data, targeter=targeter)
        handler = self.__domain.lookup_event_handler(Entity)
        return (self.__domain.__namespace__, entity, handler)
