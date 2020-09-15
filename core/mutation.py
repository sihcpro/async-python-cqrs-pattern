from datetime import datetime

from auth import UserInfo
from base import TrackingPayloadData, hashes

from .cfg import config, logger
from .datadef import Targeter
from .statemgr.state_manager import StateMgr


class Mutation:
    def __init__(self, targeter: Targeter, data: TrackingPayloadData):
        if not isinstance(targeter, Targeter):
            raise TypeError(f"targeter expect Targeter class but get {type(targeter)}")
        if isinstance(data, TrackingPayloadData):
            raise TypeError(
                f"data expect TrackingPayloadData class but get {type(data)}"
            )

        self.targeter = targeter
        self.data = data

    async def execute(self, statemgr: StateMgr, user: UserInfo):
        raise NotImplementedError


class MutationCreated(Mutation):
    async def execute(self, statemgr: StateMgr, user: UserInfo):
        ResourceClass = statemgr.lookup_resource(self.targeter.resource)
        now = datetime.utcnow()
        if issubclass(ResourceClass, TrackingPayloadData):
            return ResourceClass.extend_pclass(
                self.data,
                _created=now,
                _updated=now,
                _creator=user._id,
                _updater=user._id,
                _etag=hashes.generate_v1(config.ETAG_LENGTH),
            )
        else:
            a = ResourceClass.extend_pclass(self.data, _created=now,)
            print("--_______>", a)
            return ResourceClass.extend_pclass(self.data, _created=now,)


class MutationUpdated(Mutation):
    async def execute(self, statemgr: StateMgr, user: UserInfo):
        item = await statemgr.fetch(self.targeter.resource, self.targeter.identifier)
        if isinstance(item, TrackingPayloadData):
            return item.set(**self.data.serialize(), _updater=user._id,)
        else:
            return item.set(**self.data.serialize())


class MutationDeleted(Mutation):
    async def execute(self, statemgr: StateMgr, user: UserInfo):
        item = await statemgr.fetch(self.targeter.resource, self.targeter.identifier)
        if isinstance(item, TrackingPayloadData):
            return item.set(_deleted=self.now, _updater=user._id,)
        else:
            logger.error("You are trying to delete an un-tracking item")
            return item
