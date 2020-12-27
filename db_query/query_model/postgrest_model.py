import requests
from sanic import request

from auth import UserInfo
from base.response import AppResponse
from ..cfg import config
from ..query_builder import QueryBuilder, QueryObject
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

    def to_response(self, resp, query_obj: QueryObject, is_item=False):
        if resp.status_code // 100 == 2:
            data = resp.json()
            content_range = resp.headers.get("Content-Range", "*/*")
            content_range_length = content_range.split("/")[1]
            resp_len = 1 if content_range_length == "*" else int(content_range_length)
            return AppResponse(
                data=data,
                meta={
                    "total": resp_len,
                    "offset": query_obj["offset"],
                    "limit": query_obj["limit"],
                    "order": query_obj["order"],
                    "where": str(query_obj),
                },
                headers={"Content-Range": content_range},
            )
        else:
            return AppResponse(
                data={} if is_item else [],
                meta={"total": 0, "offset": 0, "limit": 0, "order": query_obj["order"]},
                headers={"Content-Range": "0/0"},
            )

    async def query_resource_list(
        self, request: request, user: UserInfo
    ) -> requests.Response:
        self.generate_query_data(user, request)
        query_obj = self.QUERY_BUILDER.build(self, request.args)
        resp = self.__session.get(
            self.__get_path(query_obj), headers=self.__list_header
        )
        return self.to_response(resp, query_obj)

    async def query_resource_item(
        self, request: request, user: UserInfo, identifier: str
    ) -> requests.Response:
        kwargs = {"identifier": identifier, "offset": 0}
        kwargs.update(identifier=identifier)
        self.generate_query_data(user, request)
        if self.item_is_list is False:
            kwargs["limit"] = 1
        query_obj = self.QUERY_BUILDER.build(self, request.args, **kwargs)
        resp = self.__session.get(
            self.__get_path(query_obj), headers=self.__item_header
        )
        return self.to_response(resp, query_obj)

    def __get_path(self, query_obj: str = ""):
        return f"{self.__postgrest_uri}/{self.table}{query_obj}"
