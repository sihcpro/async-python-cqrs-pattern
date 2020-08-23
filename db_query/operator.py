class Operator:
    __ops__ = {"eq": "eq"}

    @classmethod
    def get_operator(cls, list_ops: list) -> dict:
        return {op: cls.__ops__[op] for op in list_ops}
