from base import PayloadData
from base.store import Store

from .context import Context
from .entity import Entity
from .cfg import logger
from .proxy import Proxy
from typing import Tuple


class CommnadEntity(Entity):
    pass


class RootCommand(CommnadEntity):
    pass


class Command:
    __store__ = Store()

    def __init__(self, context: Context, proxy: Proxy):
        self.__context__ = context
        self.__proxy__ = proxy

        self.initiator = self.__context__.initiator
        self.data: PayloadData = None

    async def commit(self):
        logger.debug("~> Committing")
        while not self.store.is_empty:
            domain_name, cmd, data = self.pop()
            logger.debug("~~> Running %r" % cmd.__name__)
            async for aggregate in cmd(self.proxy, self.context, data):
                yield aggregate
        logger.debug("<~ Done")

    def push(self, data: Tuple[str, "function", CommnadEntity]):  # noqa: F821
        self.store.push(data)

    def pop(self) -> Tuple[str, "function", CommnadEntity]:  # noqa: F821
        return self.store.pop()

    @property
    def context(self) -> Context:
        return self.__context__

    @property
    def proxy(self) -> Proxy:
        return self.__proxy__

    @property
    def store(self) -> Store:
        return self.__store__
