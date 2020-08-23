from ..cfg import logger
from ..resource import Resource
from . import BaseState


class StateRegister(BaseState):
    @classmethod
    def _register_resource(cls, domain_name: str, resource_name: str, Res: Resource):
        logger.debug(
            "%s '%s' %s '%s'" % ("Reg", domain_name, "Resource", resource_name)
        )
        key = (domain_name, resource_name)
        if key in cls.__resource__:
            raise RuntimeError(f"Resource {resource_name} is existed!")

        cls.__resource__[key] = Res
        return Res

    def register_resource(self, resource_name: str, Res: Resource):
        return self._register_resource(self.domain.__namespace__, resource_name, Res)

    @classmethod
    def _search_resource(cls, domain_name: str, resource_name: str) -> Resource:
        key = (domain_name, resource_name)
        return cls.__resource__[key]

    def lookup_resource(self, resource_name: str) -> Resource:
        return self._search_resource(self.domain.__namespace__, resource_name)
