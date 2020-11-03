from sanic import request
from typing import List

from auth import UserInfo
from .. import field


class BaseQueryModel:
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

    _created = field.DatetimeField()

    def __init__(self):
        self.identifier: str = None
        self.keys: dict = {}
        self.default_select: str = None
        self.select_map: dict = None

        if self.__table__ is None:
            raise ValueError(f"Missing table value in '{self.__class__.__name__}'")
        if self.__endpoint__ is None:
            self.__endpoint__ = self.__table__

        for key_name in self.__dir__():
            obj: field.QueryField = getattr(self, key_name)
            if isinstance(obj, field.QueryField):
                obj.init(key_name)
                self.keys[obj.show_name] = obj
                if obj.is_identifier:
                    self.identifier = key_name

        if self.identifier is None:
            raise ValueError(f"Missing identifier in '{self.__class__.__name__}'")

    def get(self, show_name: str) -> field.QueryField:
        return self.keys.get(show_name, None)

    async def query_resource(self) -> list:
        raise NotImplementedError

    async def query_item(self, identifier: str) -> dict:
        raise NotImplementedError

    async def query_meta(self) -> list:
        raise NotImplementedError

    def base_query(self, user: UserInfo, request: request) -> dict:
        return {}

    def get_select(self, select_key: list = None) -> set:
        if not select_key:
            return self.get_default_select()

        self.select_map or self.init_select_map()
        select_list = []
        embedded_map = {}
        for show_name in select_key:
            if show_name in self.keys:
                select_list.append(self.select_map[show_name])
            else:
                first_dot = show_name.index(".")
                embedded_name = show_name[:first_dot]
                embedded_field = show_name[first_dot + 1 :]

                embedded_fielfs = embedded_map.get(embedded_name, list())
                embedded_fielfs.append(embedded_field)

        for embedded_name, embedded_field_list in embedded_map.items():
            obj = self.get(embedded_name)
            select_list.append(
                f'"{obj.show_name}":{obj.embedded_query.table}'
                f"({','.join(obj.embedded_query.get_select(embedded_field_list))})"
            )

        self.default_select = set(select_list)
        return self.default_select

    def get_default_select(self) -> set:
        if self.default_select is not None:
            return self.default_select

        self.select_map or self.init_select_map()
        self.default_select = set(self.select_map.values())
        return self.default_select

    def init_select_map(self):
        self.select_map = {}
        for show_name, obj in self.keys.items():
            self.select_map[show_name] = (
                f'"{show_name}":{obj.embedded_query.table}'
                f"({','.join(obj.embedded_query.get_default_select())})"
                if isinstance(obj, field.EmbeddedField)
                else (
                    obj.key_name
                    if obj.is_same_name
                    else f'"{show_name}".{obj.key_name}'
                )
            )
        print("-->", self.select_map)

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
