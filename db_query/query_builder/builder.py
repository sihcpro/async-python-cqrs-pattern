from json import loads
from typing import Tuple

from base.exceptions import BadRequestException
from db_query.operator import Operator
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
        query_obj = QueryObject()

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
            def dict_to_filter_str(query_key: str, query_value: str) -> Tuple:
                if ":" not in query_key:
                    query_key += ":eq"
                key_name, operator_key = query_key.split(":")

                key_obj = model_obj.get(key_name)
                if key_obj is None:
                    raise BadRequestException(
                        errcode=400851,
                        message=f"Key {key_name} is not exists in filter",
                    )
                operator = key_obj.get_operator(operator_key)

                if query_value is None:
                    query_value = "null"
                query_value = Operator.handle_value(operator, query_value)
                return key_name, operator, query_value

            query = dict()
            query.update(model_obj.default_query_data.get("where", dict()))
            query.update(url_query["where"].items())
            query.update(model_obj.base_query_data.get("where", dict()))

            where_query = {}
            for key, value in query.items():
                filter_key, operator, filter_value = dict_to_filter_str(key, value)
                where_query[filter_key] = where_query.get(filter_key, []) + [
                    f"{operator}.{filter_value}"
                ]
            query_obj["where"] = where_query

        def build_order():
            order_list = url_query["order"]
            parsed_order_list = []
            if order_list:
                for field in order_list:
                    asc = True
                    if field.startswith("!"):
                        asc = False
                        field = field[1:]

                    if model_obj.get(field) is None:
                        raise BadRequestException(
                            errcode=400854,
                            message=f"Key {field} is not exists in order",
                        )

                    parsed_order_list.append(f"{field}.{'asc' if asc else 'desc'}")

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
