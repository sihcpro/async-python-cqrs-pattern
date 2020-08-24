from sanic import request
from typing import List

from auth import UserInfo
from .. import field


class BaseQuery:
    # Register endpoint
    __table__: str = None
    __endpoint__: str = None

    __only_one__: bool = False
    __item_is_list__: bool = False
    __no_all__: bool = False
    __no_item__: bool = False
    __no_meta__: bool = False

    # Default value
    __order__: List[str] = None
    __soft_delete__: List[str] = None
    __identifier_column__: str = "_id"

    def __init__(self):
        self.identifier: str = None
        self.key: dict = {}
        self.default_select: set = set([])

        if self.__table__ is None:
            raise ValueError(f"Missing table value in '{self.__class__.__name__}'")
        if self.__endpoint__ is None:
            self.__endpoint__ = self.__table__

        for key_name in self.__dir__():
            obj: field.QueryField = getattr(self, key_name)
            if isinstance(obj, field.QueryField):
                if obj.name is None:
                    obj.name = key_name

                self.key[key_name] = obj

                if not obj.is_hidden:
                    self.default_select.add(obj.name)
                if obj.is_identifier:
                    self.identifier = key_name

        if self.identifier is None:
            raise ValueError(f"Missing identifier in '{self.__class__.__name__}'")

    def get(self, key_name: str) -> field.QueryField:
        return self.key.get(key_name, None)

    async def query_resource(self) -> list:
        raise NotImplementedError

    async def query_item(self, identifier: str) -> dict:
        raise NotImplementedError

    async def query_meta(self) -> list:
        raise NotImplementedError

    def base_query(self, user: UserInfo, request: request) -> dict:
        return {}

    @property
    def table(self):
        return self.__table__

    @property
    def endpoint(self):
        return self.__endpoint__

    @property
    def only_one(self):
        return self.__only_one__

    @property
    def item_is_list(self):
        return self.__item_is_list__

    @property
    def no_all(self):
        return self.__no_all__

    @property
    def no_item(self):
        return self.__no_item__

    @property
    def no_meta(self):
        return self.__no_meta__

    @property
    def order(self):
        return self.__order__

    @property
    def soft_delete(self):
        return self.__soft_delete__

    @property
    def identifier_column(self):
        return self.__identifier_column__
