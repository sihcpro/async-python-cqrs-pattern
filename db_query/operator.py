class Operator:
    __ops__ = {
        "search": "fts",
        "in": "in",
        "is": "is",
        "eq": "eq",
        "gt": "gt",
        "gte": "gte",
        "lt": "lt",
        "lte": "lte",
        "neq": "neq",
        "contains": "cs",
        "contained": "cd",
    }

    @classmethod
    def get_operator(cls, list_ops: list) -> dict:
        return {op: cls.__ops__[op] for op in list_ops}

    @classmethod
    def get_value(cls, op_key: str) -> str:
        return cls.__ops__.get(op_key, None)

    @classmethod
    def handle_value(cls, op_key, value) -> str:
        if op_key == "in":
            if isinstance(value, list):
                value = ",".join([str(i) for i in value])
            value = "(%s)" % value

        if op_key in ["cs", "cd"]:
            if isinstance(value, list):
                value = ",".join([str(i) for i in value])
            value = "{%s}" % value

        return value
