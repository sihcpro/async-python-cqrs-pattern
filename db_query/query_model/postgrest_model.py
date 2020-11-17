import requests
from sanic import request

from auth import UserInfo

from ..builder import QueryBuilder
from ..cfg import config
from .base_model import BaseQueryModel


class PostgrestQueryModel(BaseQueryModel):
    QUERY_BUILDER = QueryBuilder()

    NORMAL_HEADER = {"content-type": "json"}
    LIST_HEADER = {"Prefer": "count=exact", **NORMAL_HEADER}
    ITEM_HEADER = {
        "Accept": "application/vnd.pgrst.object+json",
        **NORMAL_HEADER,
    }

    def __init__(self, postgrest_uri=config.DEFAULT_POSTGREST_URI, ssl=False):
        super().__init__()
        self.__postgrest_uri = postgrest_uri
        self.__init_session(ssl)
        self.__init__header()

    def __init_session(self, ssl=False):
        self.__session = requests.Session()

    def __init__header(self):
        self.__list_header = self.ITEM_HEADER if self.only_one else self.LIST_HEADER
        self.__item_header = self.LIST_HEADER if self.item_is_list else self.ITEM_HEADER

    async def query_resource_list(
        self, request: request, user: UserInfo
    ) -> requests.Response:
        query_str = self.QUERY_BUILDER.build(
            self, request, self.base_query(user, request)
        )
        return self.__session.get(
            self.__get_path(query_str), headers=self.__list_header
        )

    async def query_resource_item(
        self, request: request, user: UserInfo, identifier: str
    ) -> requests.Response:
        query_str = self.QUERY_BUILDER.build(
            self, request, self.base_query(user, request)
        )
        return self.__session.get(
            self.__get_path(query_str), headers=self.__item_header
        )

    def __get_path(self, query_str: str = ""):
        return f"{self.__postgrest_uri}/{self.table}{query_str}"
