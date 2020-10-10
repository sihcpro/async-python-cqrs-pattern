from typing import Dict

from ..query_model import BaseQueryModel

from auth import user_auth


class QueryBase:
    maps: Dict[str, BaseQueryModel] = {}

    def __init__(
        self, app, domain: str, postgrest_url: str, authen_decorator=user_auth
    ):
        self.__app__ = app
        self.__domain__ = domain
        self.__postgrest_url__ = postgrest_url
        self.__authen_decorator__ = authen_decorator
