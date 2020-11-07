class Operator:
    __ops__ = {
        "search": "fts",
        "is": "is",
        "eq": "eq",
        "gt": "gt",
        "gte": "gte",
        "lt": "lt",
        "lte": "lte",
        "neq": "neq",
    }

    @classmethod
    def get_operator(cls, list_ops: list) -> dict:
        return {op: cls.__ops__[op] for op in list_ops}

    @classmethod
    def get_value(cls, op_key: str) -> str:
        return cls.__ops__.get(op_key, None)
