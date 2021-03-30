from __future__ import annotations

from auth.datadef import UserInfo
from .datadef import Initiator


class Context:
    def __init__(self, domain, user: UserInfo, initiator: Initiator):
        self.__domain__ = domain
        self.__initiator__ = initiator
        self.__user__ = user

    @property
    def initiator(self) -> Initiator:
        return self.__initiator__

    @property
    def user(self) -> UserInfo:
        return self.__user__
