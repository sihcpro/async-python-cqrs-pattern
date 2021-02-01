from json import loads

from base.exceptions import BadRequestException
from db_query.query_builder.object import QueryObject
from ..cfg import config
from ..query_model import BaseQueryModel


def load_query(query_url: dict, query_key: str, default=None):
    try:
        return loads(query_url.get(query_key))
    except Exception:
        return default


class QueryBuilder:
    def build(
        self, model_obj: BaseQueryModel, query_url: dict, **kwargs
    ) -> QueryObject:

        url_query = {
            "select": set(load_query(query_url, "select", list())),
            "order": set(load_query(query_url, "order", model_obj.order)),
            "where": load_query(query_url, "where", dict()),
        }
        if "identifier" in kwargs:
            url_query["where"].update({model_obj.identifier: kwargs["identifier"]})
        query_obj = QueryObject(model_obj)

        def build_select():
            # select_list = url_query["select"]

            select_list = (
                model_obj.get_select(url_query["select"])
                if url_query["select"]
                else model_obj.get_default_select()
            )
            if select_list:
                query_obj["select"] = select_list

        def build_filter():
            where_query = dict()
            where_query.update(model_obj.default_query_data.get("where", dict()))
            where_query.update(url_query["where"].items())
            where_query.update(model_obj.base_query_data.get("where", dict()))

            query_obj["where"] = where_query

        def build_order():
            order_list = url_query["order"]
            parsed_order_list = []
            if order_list:
                for field in order_list:
                    is_asc = True
                    if field.startswith("!"):
                        is_asc = False
                        field = field[1:]

                    if model_obj.get(field) is None:
                        raise BadRequestException(
                            errcode=400854,
                            message=f"Key {field} is not exists in order",
                        )

                    parsed_order_list.append(f"{field}.{'asc' if is_asc else 'desc'}")

            query_obj["order"] = parsed_order_list

        def build_object_attribute():
            query_obj["limit"] = (
                1
                if model_obj.only_one
                else (
                    model_obj.base_query_data.get("limit", None)
                    or kwargs.get("limit", None)
                    or int(load_query(query_url, "limit", 0))
                    or model_obj.default_query_data.get("limit", None)
                    or config.LIMIT
                )
            )
            query_obj["offset"] = (
                model_obj.base_query_data.get("offset", None)
                or kwargs.get("offset", None)
                or int(load_query(query_url, "offset", 0))
                or model_obj.default_query_data.get("offset", 0)
            )

        build_select()
        build_filter()
        build_order()
        build_object_attribute()

        return query_obj
