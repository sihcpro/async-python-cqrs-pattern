from typing import List, Tuple

from base.identifier import UUID_GENR
from base.store import Store

from .cfg import logger
from .datadef import Targeter, field
from .entity import Entity
from .mutation import Mutation
from .statemgr.state_manager import StateMgr


class EventEntity(Entity):
    targeter: Targeter = field(Targeter, mandatory=True)


class Event:
    __store__: Store = Store()

    def __init__(self, domain, statemgr: StateMgr):
        self._id = UUID_GENR()

        self.__domain = domain
        self.__statemgr = statemgr

    async def execute(self, event_store: Tuple[str, EventEntity, List[Mutation]]):
        _, entity, event_handler = event_store
        logger.debug("~~~~> Running '%r'" % event_handler.__name__)

        async for mutation in event_handler(self.statemgr, entity):
            return self.__statemgr.save(
                await mutation.execute(self.statemgr, self.__domain.context.user)
            )

    async def commit(self):
        logger.debug("~> Committing")
        while not self.__store__.is_empty:
            yield await self.execute(self.__store__.pop())
        logger.debug("<~ Done")

    def push(self, data: tuple):
        self.__store__.push(data)

    @property
    def statemgr(self):
        return self.__statemgr
