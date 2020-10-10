from auth import UserInfo
from base.response_handler import ResponseHandler
from base.response import AppResponse

from ..cfg import logger
from ..query_model import BaseQueryModel
from .query_base import QueryBase


class QueryRegister(QueryBase):
    def register(self, QueryModel: BaseQueryModel, authen_decorator=None):
        object_authen = (
            authen_decorator
            if authen_decorator is not None
            else self.__authen_decorator__
        )
        self.obj: BaseQueryModel = QueryModel(self.__postgrest_url__)
        self.maps[self.obj.endpoint] = self.obj
        logger.info(
            f"Register query endpoint '{self.__domain__}/{self.obj.endpoint}' "
            f"with table '{self.obj.table}'"
        )

        resource_path = f"/{self.__domain__}/{self.obj.endpoint}"
        item_path = f"{resource_path}/<identifier>"
        meta_path = rf"{resource_path}(.*):meta"

        @ResponseHandler.handler
        @object_authen
        async def register_query_resource(request, user: UserInfo):
            resp = await self.obj.query_resource(request, user)
            return AppResponse(data=resp)

        @ResponseHandler.handler
        @object_authen
        async def register_query_item(request, user: UserInfo, identifier: str):
            resp = await self.obj.query_item(request, user, identifier)
            return AppResponse(data=resp)

        @ResponseHandler.handler
        async def register_query_meta(request):
            resp = await self.obj.meta()
            return resp

        if self.obj.only_one:
            self.__app__.add_route(
                register_query_resource, resource_path, methods=["GET"]
            )
        else:
            if self.obj.no_all is False:
                self.__app__.add_route(
                    register_query_resource, resource_path, methods=["GET"]
                )
            if self.obj.no_item is False:
                self.__app__.add_route(register_query_item, item_path, methods=["GET"])
            if self.obj.no_meta is False:
                self.__app__.add_route(register_query_meta, meta_path, methods=["GET"])
