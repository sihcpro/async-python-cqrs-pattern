from .operator import Operator


class QueryField:
    __allowed_operator__: list = []

    def __init__(
        self,
        show_name: str = None,
        identifier: bool = False,
        hidden: bool = False,
        **kwargs
    ):
        self.key_name: str = None
        self.source = kwargs.get("source", "root")
        self.show_name = show_name
        self.is_same_name = None
        self.is_identifier = identifier
        self.is_hidden = hidden

        self.__operator__ = Operator.get_operator(self.__allowed_operator__)

    def init(self, key_name: str):
        self.key_name = key_name
        self.is_same_name = False
        if self.show_name is None:
            self.show_name = self.key_name
            self.is_same_name = True

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
    def __init__(self, EmbeddedQueryClass, foreign_key: str = None, **kwargs):
        self.foreign_key = foreign_key
        self.embedded_query = EmbeddedQueryClass()
        super().__init__(source=self.embedded_query.endpoint, **kwargs)


class TextSearchField(QueryField):
    __allowed_operator__ = ["search"]
