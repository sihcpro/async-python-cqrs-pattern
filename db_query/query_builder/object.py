from typing import Any


class QueryObject(dict):
    def __init__(self):
        super().__init__()
        self.attributes: dict = dict()

    def __setitem__(self, name: str, value: Any) -> None:
        super(QueryObject, self).__setitem__(name, value)
        self.attributes[name] = value

    def build_where(self, query: list) -> str:
        query_list = []
        for key, values in query.items():
            for value in values:
                query_list.append(f"{key}={value}")
        return "&".join(query_list)

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
