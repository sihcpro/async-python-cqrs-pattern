from base import db, UUID_TYPE
from base.exceptions import NotFoundException

from ..datadef import ResourceData
from ..resource import Resource
from .state_store import StateStore


class StateConnector(StateStore):
    __db__ = db

    async def fetch_from_db(self, resource: str, identifier: UUID_TYPE) -> Resource:
        ResourceModel = self.lookup_resource(resource)
        item = await ResourceModel.__model__.get(identifier)
        if item is None:
            raise NotFoundException(
                errcode=404904, data={"resource": resource, "identifier": identifier}
            )
        result = ResourceModel.create(item.__values__)
        self.keep(result)
        return result

    async def fetch(self, resource: str, identifier: UUID_TYPE) -> Resource:
        return self.fetch_from_store(resource, identifier) or await self.fetch_from_db(
            resource, identifier
        )

    async def fetch_target(self, target: ResourceData) -> Resource:
        return await self.fetch(target.resource, target.identifier)
