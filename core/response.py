from pyrsistent import field

from base.response import AppResponse
from base.store import Store

from .cfg import logger
from .entity import Entity


class BaseResponse(Entity):
    data = field(dict, initial=dict, mandatory=True)
    status = field(int, initial=200, mandatory=True)
    message = field(str, initial="OK", mandatory=True)

    async def execute(self):
        raise NotImplementedError


class JsonResponse(BaseResponse):
    async def execute(self):
        return AppResponse(
            body={"status": self.status, "data": self.data, "message": self.message},
            status=self.status,
        )


class Response:
    __store__: Store = Store()

    async def commit(self) -> AppResponse:
        logger.debug("~> Committing")
        while not self.__store__.is_empty:
            domain_name, entity, response_handler = self.__store__.pop()
            logger.debug(
                "~~> Running %r", (response_handler.__name__, entity.__class__.__name__)
            )

            yield await response_handler(entity)
        logger.debug("<~ Done")

    # @TODO: make it fucking complicated, please! @@
    def push(self, data: tuple):
        self.__store__.push(data)
