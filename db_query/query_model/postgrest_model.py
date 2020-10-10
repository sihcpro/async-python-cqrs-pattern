import requests
from sanic import request

from auth import UserInfo

from ..builder import QueryBuilder
from ..cfg import config
from .base_model import BaseQueryModel


class PostgrestQueryModel(BaseQueryModel):
    query_builder = QueryBuilder()

    def __init__(self, postgrest_uri=config.DEFAULT_POSTGREST_URI, ssl=False):
        super().__init__()
        self.__postgrest_uri = postgrest_uri
        self.__init_session(ssl)
        self.__init__header()

    def __init_session(self, ssl=False):
        self.__session = requests.Session()

    def __init__header(self):
        normal_response = {"content-type": "json"}
        only_one_response = {
            "Accept": "application/vnd.pgrst.object+json",
            **normal_response,
        }
        self.__resource_header = only_one_response if self.only_one else normal_response
        self.__item_header = normal_response if self.item_is_list else only_one_response

    async def query_resource(self, request: request, user: UserInfo) -> list:
        query_str = self.query_builder.build(
            self, request, self.base_query(user, request)
        )
        resp = self.__session.get(
            self.__get_path(query_str), headers=self.__resource_header
        )
        return resp.json()

    async def query_item(
        self, request: request, user: UserInfo, identifier: str
    ) -> list:
        query_str = self.query_builder.build(
            self, request, self.base_query(user, request)
        )
        resp = self.__session.get(
            self.__get_path(query_str), headers=self.__item_header
        )
        return resp.json()

    def __get_path(self, query_str: str = ""):
        return f"{self.__postgrest_uri}/{self.table}{query_str}"
