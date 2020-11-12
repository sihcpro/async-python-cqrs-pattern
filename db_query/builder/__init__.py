from base.exceptions import BadRequestException
from json import loads

from ..cfg import logger, config
from ..query_model import BaseQueryModel


def load_query(query_url: dict, query_key: str, default=None):
    try:
        return loads(query_url.args.get(query_key))
    except Exception:
        return default


class QueryBuilder:
    def build(
        self, query_obj: BaseQueryModel, query_url: dict, base_query: dict
    ) -> str:
        url_query = {
            "select": set(load_query(query_url, "select", [])),
            "order": set(load_query(query_url, "order", [])),
            "where": load_query(query_url, "where", {}),
            "limit": int(
                load_query(query_url, "limit", base_query.get("limit", config.LIMIT))
            ),
            "offset": int(load_query(query_url, "offset", base_query.get("offset", 0))),
        }

        def build_select():
            # select_list = url_query["select"]

            select_list = query_obj.get_select(url_query["select"])

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

                if query_value is None:
                    query_value = "null"
                return f"{key_obj.key_name}={operator}.{query_value}"

            aggregate_query = []

            if url_query["where"]:
                for key, item in url_query["where"].items():
                    aggregate_query.append(dict_to_filter_str(key, item))
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
                url_query["limit"] = 1

            obj_query.append(f"limit={url_query['limit']}")
            obj_query.append(f"offset={url_query['offset']}")

            return obj_query

        query_list = []
        query_list.extend(build_select())
        query_list.extend(build_filter())
        query_list.extend(build_order())
        query_list.extend(build_object_attribute())

        query_str = "?" + "&".join(query_list)
        logger.debug("query str: %r", query_str)
        return query_str
