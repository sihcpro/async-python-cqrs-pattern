from base.exceptions import BadRequestException
from json import loads

from ..cfg import logger
from ..query import BaseQuery


class QueryBuilder:
    def build(self, query_obj: BaseQuery, query_url: dict, base_query: dict) -> str:
        def build_select():
            try:
                select_list = set(loads(query_url.args.get("select")))
            except Exception:
                select_list = set([])

            if select_list:
                if select_list.issubset(query_obj.default_select) is False:
                    raise BadRequestException(
                        errcode=400853,
                        message=(
                            f"Field {select_list - query_obj.default_select} "
                            "is not exists"
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
                        errcode=400851, message=f"Key {key_name} is not exists"
                    )
                operator = key_obj.get_operator(operator_key)
                if operator is None:
                    raise BadRequestException(
                        errcode=400852, message=f"Operator {operator_key} is not exists"
                    )

                return f"{key_obj.name}={operator}.{query_value}"

            aggregate_query = []
            if "where" in base_query:
                for key, item in base_query["where"].items():
                    aggregate_query.append(dict_to_filter_str(key, item))
            return aggregate_query

        def build_order():
            aggregate_query = []
            return aggregate_query

        query_list = []
        query_list.extend(build_select())
        query_list.extend(build_filter())
        query_list.extend(build_order())

        query_str = "?" + "&".join(query_list)
        logger.debug("query str: %r", query_str)
        return query_str
