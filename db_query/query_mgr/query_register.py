from base.response_handler import ResponseHandler

from auth import UserInfo
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
        obj: BaseQueryModel = QueryModel(self.__postgrest_url__)
        self.maps[obj.endpoint] = obj
        resource_path = f"/{self.__domain__}/{obj.endpoint}"
        item_path = f"{resource_path}/<identifier>"
        meta_path = rf"{resource_path}(.*):meta"

        logger.info(
            f"Register query endpoint '{resource_path}' with table '{obj.table}'"
        )

        @ResponseHandler.handler
        @object_authen
        async def register_query_resource_list(request, user: UserInfo):
            return await obj.query_resource_list(request, user)

        @ResponseHandler.handler
        @object_authen
        async def register_query_resource_item(
            request, user: UserInfo, identifier: str
        ):
            return await obj.query_resource_item(request, user, identifier)

        @ResponseHandler.handler
        async def register_query_meta(request):
            resp = await obj.meta()
            return resp

        if obj.only_one:
            self.__app__.add_route(
                register_query_resource_list, resource_path, methods=["GET"]
            )
        else:
            if obj.no_all is False:
                self.__app__.add_route(
                    register_query_resource_list, resource_path, methods=["GET"]
                )
            if obj.no_item is False:
                self.__app__.add_route(
                    register_query_resource_item, item_path, methods=["GET"]
                )
            if obj.no_meta is False:
                self.__app__.add_route(register_query_meta, meta_path, methods=["GET"])
