from typing import Dict, Tuple

from ..domain import BaseDomain
from ..resource import Resource


class BaseState:
    __resource__: Dict[Tuple[str, str], Resource] = {}

    def __init__(self, domain: BaseDomain):
        self.__domain = domain

    @property
    def resource(self) -> Resource:
        return self.__resource__

    @property
    def domain(self) -> str:
        return self.__domain
