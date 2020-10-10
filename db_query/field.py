from .operator import Operator


class QueryField:
    __allowed_operator__: list = []

    def __init__(
        self, name: str = None, identifier: bool = False, hidden: bool = False, **kwargs
    ):
        self.source = kwargs.get("source", "root")
        self.name = name
        self.is_identifier = identifier
        self.is_hidden = hidden

        self.__operator__ = Operator.get_operator(self.__allowed_operator__)

    @classmethod
    def get_operator(cls, operator_name: str) -> str:
        return Operator.get_value(operator_name)


class IntField(QueryField):
    __allowed_operator__ = ["eq"]


class BooleanField(QueryField):
    __allowed_operator__ = ["eq"]


class FloatField(QueryField):
    __allowed_operator__ = ["eq"]


class StringField(QueryField):
    __allowed_operator__ = ["eq"]


class DatetimeField(StringField):
    pass


class UUIDField(StringField):
    pass


class ArrayField(QueryField):
    pass


class JsonField(QueryField):
    pass


class EmbeddedField(QueryField):
    def __init__(self, source, foreign_key, **kwargs):
        self.foreign_key = foreign_key
        super().__init__(source=source, **kwargs)


class TextSearchField(QueryField):
    __allowed_operator__ = ["search"]
