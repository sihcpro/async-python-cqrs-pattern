from sanic import request
from typing import Dict, List

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
    __order__: List[str] = []
    __soft_delete__: List[str] = None
    __identifier_column__: str = "_id"

    _etag = field.DatetimeField(hidden=True)

    def __init__(self):
        self.identifier: str = None
        self.keys: Dict[str, field.QueryField] = {}
        self.default_select: str = None
        self.select_map: dict = None
        self.default_query_data: dict = None
        self.base_query_data: dict = None

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
        dot_position = show_name.find(".")
        if dot_position == -1:
            return self.keys.get(show_name, None)
        else:
            embedded_name = show_name[:dot_position]
            field_name = show_name[dot_position + 1 :]
            key: field.EmbeddedField = self.keys.get(embedded_name, None)
            return key.embedded_query.get(field_name)

    async def query_resource_list(self) -> list:
        raise NotImplementedError

    async def query_resource_item(self, identifier: str) -> dict:
        raise NotImplementedError

    async def query_meta(self) -> list:
        raise NotImplementedError

    async def get_extra_data(self, user: UserInfo, request: request) -> dict:
        return {}

    def default_query(self, user: UserInfo, request: request) -> dict:
        return {}

    def base_query(self, user: UserInfo, request: request) -> dict:
        return {}

    async def generate_query_data(self, user: UserInfo, request: request):
        self.extra_data = await self.get_extra_data(user, request)
        self.default_query_data = self.default_query(user, request)
        self.base_query_data = self.base_query(user, request)

    def get_select(self, select_key: list) -> set:
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
                f'"{obj.show_name}":"{obj.embedded_query.table}"'
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
            if obj.is_hidden:
                continue
            self.select_map[show_name] = (
                f'"{show_name}":"{obj.embedded_query.table}"'
                f"({','.join(obj.embedded_query.get_default_select())})"
                if isinstance(obj, field.EmbeddedField)
                else (
                    obj.key_name
                    if obj.is_same_name
                    else f'"{show_name}":"{obj.key_name}"'
                )
            )

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
