from typing import Dict, Tuple

from base.helper import pascal_to_snake_case

from ..entity import Entity
from ..cfg import logger
from ..resource import Resource
from ..statemgr.state_manager import StateMgr
from . import BaseDomain


class DomainRegister(BaseDomain):
    __statemgr__ = StateMgr
    __entity__: Dict[Tuple[str, str], Entity] = {}

    @property
    def statemgr(cls) -> StateMgr:
        return cls.__statemgr__

    @property
    def entity(self) -> Dict[Tuple[str, str], Entity]:
        return self.__entity__

    @classmethod
    def register_resource(cls, Res: Resource) -> Resource:
        return cls.__statemgr__._register_resource(
            cls.__namespace__, Res.__resource_name__, Res
        )

    def lookup_resource(self, resource_name: str) -> Resource:
        return self.__statemgr__.lookup_resource(self.__namespace__, resource_name)

    @classmethod
    def register_entity(cls, name_or_cls):
        name = name_or_cls

        def _register_entity(entity: Entity) -> Entity:
            logger.debug("%s '%s' %s '%s'" % ("Reg", cls.__namespace__, "Enti", name))
            if name in cls.__entity__:
                raise RuntimeError(f"Entity {name} is existed!")

            cls.__entity__[(cls.__namespace__, name)] = entity
            return entity

        if not isinstance(name_or_cls, str):
            name = pascal_to_snake_case(name_or_cls.__name__)
            return _register_entity(name_or_cls)
        return _register_entity

    @classmethod
    def lookup_entity(cls, entity_name) -> Entity:
        key = (cls.__namespace__, entity_name)
        return cls.__entity__[key]
