from json import loads

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
        self, model_obj: BaseQueryModel, query_url: dict, base_query: dict, **kwargs
    ) -> QueryObject:
        query_url.update(kwargs)
        url_query = {
            "select": set(load_query(query_url, "select", [])),
            "order": set(load_query(query_url, "order", model_obj.order)),
            "where": load_query(query_url, "where", {}),
            "limit": int(
                load_query(query_url, "limit", base_query.get("limit", config.LIMIT))
            ),
            "offset": int(load_query(query_url, "offset", base_query.get("offset", 0))),
            "identifier": query_url.get("identifier", None),
        }
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
            def dict_to_filter_str(query_key: str, query_value: str) -> str:
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
                return key_name, f"{operator}.{query_value}"

            if url_query["where"]:
                for key, value in url_query["where"].items():
                    filter_key, filter_value = dict_to_filter_str(key, value)
                    query_obj[filter_key] = filter_value
            if "where" in base_query:
                for key, value in base_query["where"].items():
                    filter_key, filter_value = dict_to_filter_str(key, value)
                    query_obj[filter_key] = filter_value
            if url_query["identifier"] is not None:
                query_obj[model_obj.identifier] = f"eq.{url_query['identifier']}"

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
            if model_obj.only_one:
                url_query["limit"] = 1

            query_obj["limit"] = url_query["limit"]
            query_obj["offset"] = url_query["offset"]

        build_select()
        build_filter()
        build_order()
        build_object_attribute()

        return query_obj
