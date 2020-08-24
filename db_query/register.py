from auth import user_auth, UserInfo
from base.response_handler import ResponseHandler
from base.response import AppResponse

from .query import BaseQuery
from .cfg import logger


def register_query_domain(
    app, domain: str, backend: str, authen_decorator=user_auth
) -> BaseQuery:
    logger.info(f"Register domain '{domain}' with backend '{backend}'")

    def _register_query_model(QueryModel: BaseQuery) -> BaseQuery:
        query_obj = QueryModel(domain, backend)
        logger.info(
            f"Register query endpoint '{domain}/{query_obj.endpoint}' "
            f"with table '{query_obj.table}'"
        )

        resource_path = f"/{domain}/{query_obj.endpoint}"
        item_path = f"{resource_path}/<identifier>"
        meta_path = rf"{resource_path}(.*):meta"

        @ResponseHandler.handler
        @authen_decorator
        async def register_query_resource(request, user: UserInfo):
            resp = await query_obj.query_resource(request, user)
            return AppResponse(data=resp)

        @ResponseHandler.handler
        @authen_decorator
        async def register_query_item(request, user: UserInfo, identifier: str):
            resp = await query_obj.query_item(request, user, identifier)
            return AppResponse(data=resp)

        @ResponseHandler.handler
        async def register_query_meta(request):
            resp = await query_obj.meta()
            return resp

        if query_obj.only_one:
            app.add_route(register_query_resource, resource_path, methods=["GET"])
        else:
            if query_obj.no_all is False:
                app.add_route(register_query_resource, resource_path, methods=["GET"])
            if query_obj.no_item is False:
                app.add_route(register_query_item, item_path, methods=["GET"])
            if query_obj.no_meta is False:
                app.add_route(register_query_meta, meta_path, methods=["GET"])

    return _register_query_model
