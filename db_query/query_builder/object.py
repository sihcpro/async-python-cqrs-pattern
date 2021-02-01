from typing import Any, Tuple

from base.exceptions import BadRequestException
from db_query.operator import Operator
from db_query.query_model.base_model import BaseQueryModel


class QueryObject(dict):
    special_key = {"and", "or", "!and", "or"}

    def __init__(self, model_obj: BaseQueryModel):
        super().__init__()
        self.model_obj = model_obj
        self.attributes: dict = dict()

    def __setitem__(self, name: str, value: Any) -> None:
        super(QueryObject, self).__setitem__(name, value)
        self.attributes[name] = value

    def build_where(self, query: list) -> str:
        def handler_oprator(operator) -> str:
            if operator[0] == "!":
                operator = f"not.{operator[1:]}"
            return operator

        def dict_to_filter_str(query_key: str, query_value: str) -> Tuple:
            if ":" not in query_key:
                query_key += ":eq"
            key_name, operator_key = query_key.split(":")

            key_obj = self.model_obj.get(key_name)
            if key_obj is None:
                raise BadRequestException(
                    errcode=400851,
                    message=f"Key {key_name} is not exists in filter",
                )
            operator = key_obj.get_operator(operator_key)
            operator = handler_oprator(operator)

            if query_value is None:
                query_value = "null"
            query_value = Operator.handle_value(operator, query_value)
            return key_name, operator, query_value

        def build(query: list, layer=0):
            query_list = []
            for key, value in query.items():
                if key in self.special_key:
                    operator = handler_oprator(key)
                    query_str = (
                        f"{operator}=({','.join(build(value, layer=layer + 1))})"
                    )
                else:
                    if layer == 0:
                        filter_key, operator, filter_value = dict_to_filter_str(
                            key, value
                        )
                        query_str = f"{filter_key}={operator}.{filter_value}"
                    else:
                        filter_key, operator, filter_value = dict_to_filter_str(
                            key, value
                        )
                        query_str = f"{filter_key}.{operator}.{filter_value}"
                query_list.append(query_str)
            return query_list

        query_list_builded = build(query)
        return "&".join(query_list_builded)

    def __str__(self):
        query_list = []
        for key, value in self.attributes.items():
            if not value:
                continue
            if key == "where":
                query_list.append(self.build_where(value))
            elif isinstance(value, (set, list)):
                query_list.append(f"{key}={','.join(value)}")
            else:
                query_list.append(f"{key}={value}")
        query_str = "?" + "&".join(query_list)
        return query_str
