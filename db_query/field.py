from base.exceptions import BadRequestException

from .operator import Operator


class QueryField:
    __allowed_operator__: set = {"in"}

    def __init__(
        self,
        show_name: str = None,
        identifier: bool = False,
        hidden: bool = False,
        **kwargs,
    ):
        self.key_name: str = None
        self.source = kwargs.get("source", "root")
        self.show_name = show_name
        self.is_same_name: bool = None
        self.is_identifier = identifier
        self.is_hidden = hidden

        self.__operator__ = Operator.get_operator(self.__allowed_operator__)

    def init(self, key_name: str):
        self.key_name = key_name
        if self.show_name is None:
            self.show_name = self.key_name
        self.is_same_name = self.show_name == self.key_name

    @classmethod
    def get_operator(cls, operator_name: str) -> str:
        operator_value = Operator.get_value(operator_name)
        if operator_value is None:
            raise BadRequestException(
                errcode=400852,
                message=f"Operator {operator_value} is not exists in filter",
            )
        return operator_value


class BooleanField(QueryField):
    __allowed_operator__ = {"in", "is", "eq", "neq"}


class IntField(QueryField):
    __allowed_operator__ = {"in", "is", "eq", "neq", "gt", "gte", "lt", "lte"}


class FloatField(IntField):
    pass


class DateField(IntField):
    pass


class DatetimeField(IntField):
    pass


class StringField(QueryField):
    __allowed_operator__ = {"in", "is", "eq", "neq"}


class UUIDField(StringField):
    pass


class ArrayField(QueryField):
    __allowed_operator__ = {"contains", "contained"}


class JsonField(QueryField):
    pass


class TextSearchField(QueryField):
    __allowed_operator__ = ["search"]


class EmbeddedField(QueryField):
    def __init__(self, EmbeddedQueryClass, foreign_key: str = None, **kwargs):
        self.foreign_key = foreign_key
        self.embedded_query = EmbeddedQueryClass()
        super().__init__(source=self.embedded_query.endpoint, **kwargs)
