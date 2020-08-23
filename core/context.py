from __future__ import annotations

from auth.datadef import UserInfo
from base.identifier import UUID_GENR

from .datadef import Initiator


class Context:
    def __init__(self, domain, user: UserInfo, initiator: Initiator):
        self.__domain__ = domain
        self.__initiator__ = initiator
        self.__user__ = user

        self._id = UUID_GENR()

    @property
    def initiator(self) -> Initiator:
        return self.__initiator__

    @property
    def user(self) -> UserInfo:
        return self.__user__
