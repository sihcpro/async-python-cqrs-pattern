from datetime import datetime
from typing import Dict, Tuple

from base import UUID_TYPE, db, hashes

from ..cfg import config, logger
from ..resource import TrackingResource, Resource
from . import BaseState


class StateStore(BaseState):
    __store__: Dict[Tuple[str, str, UUID_TYPE], TrackingResource] = {}
    __origin__: Dict[Tuple[str, str, UUID_TYPE], TrackingResource] = {}

    def keep(self, item: TrackingResource):
        key = (self.domain.__namespace__, item.__resource_name__, item._id)
        if key not in self.origin:
            self.origin[key] = item
            self.store[key] = item

    def save(self, item: TrackingResource):
        key = (self.domain.__namespace__, item.__resource_name__, item._id)
        logger.debug("~~~~~> Saving: %r", key)
        if key not in self.store or isinstance(item, Resource):
            logger.debug("<~~~~~ Saved")
            self.store[key] = item
            return
        if self.store[key]._etag != item._etag:
            raise RuntimeError(f"Item {key} had been updated")
        if self.store[key] != item:
            logger.debug("<~~~~~ Saved")
            self.store[key] = item.set(
                _updated=datetime.utcnow(), _etag=hashes.generate_v1(config.ETAG_LENGTH)
            )

    def fetch_from_store(
        self, resource: str, identifier: UUID_TYPE
    ) -> TrackingResource:
        key = (self.domain.__namespace__, resource, identifier)
        return self.store.get(key, None)

    async def commit(self):
        logger.debug("~> Commiting")
        for key, item in self.store.items():
            logger.debug("~~> Key: %r", key)
            if key not in self.origin:
                logger.debug(f"<~~ Created {item.__class__.__name__}")
                Model = item.__backend__

                result = await Model.create(**item.serialize())
                yield (f"Created {key}", result)
            elif (
                isinstance(item, TrackingResource)
                and item._etag != self.origin[key]._etag
            ):
                logger.debug(f"<~~ Updated {item.__class__.__name__}")
                Model = item.__backend__

                result = (
                    await Model.update.values(**item.serialize())
                    .where(
                        db.and_(
                            Model._id == item._id, Model._etag == self.origin[key]._etag
                        )
                    )
                    .gino.status()
                )
                yield (f"Updated {key}", result)
            elif isinstance(item, Resource) and item is not self.origin[key]:
                logger.debug(f"<~~ Updated {item.__class__.__name__} Resource")
                Model = item.__backend__

                result = (
                    await Model.update.values(**item.serialize())
                    .where(Model._id == item._id)
                    .gino.status()
                )
                yield (f"Updated {key} Resource", result)
            else:
                logger.debug("<~~ Skiped")
        logger.debug("<~ Done")
        self.store.clear()
        self.origin.clear()

    @property
    def store(self):
        return self.__store__

    @property
    def origin(self):
        return self.__origin__
