from typing import Any, List, Tuple

from auth.datadef import UserInfo
from base.model import db
from base.store import Store
from ..cfg import logger
from ..command import Command
from ..context import Context
from ..datadef import Initiator
from ..entity import Entity
from ..event import Event, EventEntity
from ..proxy import Proxy
from ..response import BaseResponse, Response
from ..statemgr.state_manager import StateMgr
from .domain_handler import DomainHandler
from .domain_register import DomainRegister


class DomainProcess(DomainRegister, DomainHandler):
    def __init__(self, user: UserInfo, initiator: Initiator):
        self.__store__ = Store()
        self.__context__ = Context(self, user, initiator)
        self.__response__ = Response()
        self.__statemgr__ = StateMgr(self)
        self.__proxy__ = Proxy(self, self.__statemgr__)
        self.__command__ = Command(self.__context__, self.__proxy__)
        self.__event__ = Event(self, self.__statemgr__)

    def process_command(self, entity_name: str, data: dict):
        logger.debug("> Process command")
        Entity = self.lookup_entity(entity_name)
        entity = Entity(data=data)
        command = self.lookup_command_handler(Entity)
        self.command.push((self.__namespace__, command, entity))
        # command = self.lookup_command_handler(entity)
        # [command_process for command_process in command.commit()]

    async def commit(self) -> List[BaseResponse]:
        async def distribute_aggregate(aggregate: Tuple[str, Entity, Any]):
            if aggregate is None:
                return
            logger.debug(
                "~~~> Aggregate: %r"
                % (
                    (
                        aggregate[0],
                        aggregate[1].__class__.__name__,
                        aggregate[2].__name__,
                    ),
                )
            )
            if isinstance(aggregate[1], EventEntity):
                await self.event.execute(aggregate)
            if isinstance(aggregate[1], BaseResponse):
                self.response.push(aggregate)

        async def _commit():
            async for aggregate in self.command.commit():
                await distribute_aggregate(aggregate)
            # await self.event.commit()
            state_msg = [result async for result in self.statemgr.commit()]
            logger.info(">>>> State_msg: \n%r", state_msg)
            return [resp async for resp in self.response.commit()]

        async with db.transaction():
            return await _commit()

    @property
    def command(self) -> Command:
        return self.__command__

    @property
    def event(self) -> Event:
        return self.__event__

    @property
    def store(self) -> Store:
        return self.__store__

    @property
    def context(self) -> Context:
        return self.__context__

    @property
    def response(self) -> Response:
        return self.__response__

    @property
    def proxy(self) -> Proxy:
        return self.__proxy__
