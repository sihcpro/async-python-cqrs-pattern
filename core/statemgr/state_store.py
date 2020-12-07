from datetime import datetime
from typing import Dict, Tuple

from base import UUID_TYPE, db, hashes

from ..cfg import config, logger
from ..resource import BaseResource
from . import BaseState


class StateStore(BaseState):
    __store__: Dict[Tuple[str, str, UUID_TYPE], BaseResource] = {}
    __origin__: Dict[Tuple[str, str, UUID_TYPE], BaseResource] = {}

    def keep(self, item: BaseResource):
        key = (self.domain.__namespace__, item.__resource_name__, item._id)
        if key not in self.origin:
            self.origin[key] = item
            self.store[key] = item

    def save(self, item: BaseResource):
        assert isinstance(item, BaseResource), "Item is not a Resource"

        key = (self.domain.__namespace__, item.__resource_name__, item._id)
        logger.debug("~~~~~> Saving: %r", key)
        if key not in self.store:
            logger.debug("<~~~~~ Saved new item")
            self.store[key] = item
            return

        assert self.store[key]._etag == item._etag, f"Item {key} had been updated"
        if self.store[key] != item:
            logger.debug("<~~~~~ Saved updated item")
            self.store[key] = item.set(
                _updated=datetime.utcnow(), _etag=hashes.generate_v1(config.ETAG_LENGTH)
            )
            return

        logger.debug("<~~~~~ Skipped item")

    def fetch_from_store(self, resource: str, identifier: UUID_TYPE) -> BaseResource:
        key = (self.domain.__namespace__, resource, identifier)
        return self.store.get(key, None)

    async def commit(self):
        logger.debug("~> Commiting")
        for key, item in self.store.items():
            logger.debug("~~> Key: %r", key)
            Model = item.__model__

            # Create
            if key not in self.origin and item._created is not None:
                logger.debug(f"<~~ Created {item.__class__.__name__}")

                result = await Model.create(**item.serialize())
                yield (f"Created {key}", result)
            # Hard delete
            elif item._created is None:
                if key not in self.origin:
                    logger.debug("<~~ Skipped")
                    continue
                else:
                    logger.debug(f"<~~ Deleted {item.__class__.__name__}")
                    result = await Model.delete.where(
                        db.and_(
                            Model._id == item._id,
                            Model._etag == self.origin[key]._etag,
                        )
                    ).gino.status()
                    yield (f"Deleted {key}", result)
            # Update or soft delete
            elif item._etag != self.origin[key]._etag:
                logger.debug(f"<~~ Updated {item.__class__.__name__}")

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
            # elif isinstance(item, Resource) and item is not self.origin[key]:
            #     logger.debug(f"<~~ Updated {item.__class__.__name__} Resource")
            #     Model = item.__model__

            #     result = (
            #         await Model.update.values(**item.serialize())
            #         .where(Model._id == item._id)
            #         .gino.status()
            #     )
            #     yield (f"Updated {key} Resource", result)
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
