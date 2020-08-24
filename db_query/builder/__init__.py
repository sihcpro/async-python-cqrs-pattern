from base.exceptions import BadRequestException
from json import loads

from ..cfg import logger
from ..query import BaseQuery


class QueryBuilder:
    def build(self, query_obj: BaseQuery, query_url: dict, base_query: dict) -> str:
        url_query = {
            "select": set(loads(query_url.args.get("select", "[]"))),
            "order": set(loads(query_url.args.get("order", "[]"))),
        }

        def build_select():
            select_list = url_query["select"]

            if select_list:
                if select_list.issubset(query_obj.default_select) is False:
                    raise BadRequestException(
                        errcode=400853,
                        message=(
                            f"Field {select_list - query_obj.default_select} "
                            "is not exists in select"
                        ),
                    )
            else:
                select_list = query_obj.default_select

            if select_list:
                return ["select=" + ",".join(select_list)]
            else:
                return []

        def build_filter():
            def dict_to_filter_str(query_key: str, query_value: str) -> str:
                key_name, operator_key = query_key.split(":")

                key_obj = query_obj.get(key_name)
                if key_obj is None:
                    raise BadRequestException(
                        errcode=400851,
                        message=f"Key {key_name} is not exists in filter",
                    )
                operator = key_obj.get_operator(operator_key)
                if operator is None:
                    raise BadRequestException(
                        errcode=400852,
                        message=f"Operator {operator_key} is not exists in filter",
                    )

                return f"{key_obj.name}={operator}.{query_value}"

            aggregate_query = []
            if "where" in base_query:
                for key, item in base_query["where"].items():
                    aggregate_query.append(dict_to_filter_str(key, item))
            return aggregate_query

        def build_order():
            order_list = url_query["order"] if url_query["order"] else query_obj.order
            parsed_order_list = []
            if order_list:
                for field in order_list:
                    asc = True
                    if field.startswith("!"):
                        asc = False
                        field = field[1:]

                    if query_obj.get(field) is None:
                        raise BadRequestException(
                            errcode=400854,
                            message=f"Key {field} is not exists in order",
                        )

                    parsed_order_list.append(f"{field}.{'asc' if asc else 'desc'}")

            if parsed_order_list:
                return [f"order={','.join(parsed_order_list)}"]
            return []

        def build_object_attribute():
            obj_query = []
            if query_obj.only_one:
                obj_query.append("limit=1")
            return obj_query

        query_list = []
        query_list.extend(build_select())
        query_list.extend(build_filter())
        query_list.extend(build_order())
        query_list.extend(build_object_attribute())

        query_str = "?" + "&".join(query_list)
        logger.debug("query str: %r", query_str)
        return query_str
