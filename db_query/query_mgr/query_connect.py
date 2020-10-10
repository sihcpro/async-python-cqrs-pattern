# from typing import Dict

# from .. import field
# from ..cfg import logger
# from ..query_model import BaseQueryModel
# from .query_base import QueryBase


# class QueryConnect(QueryBase):
#     select_maps: Dict[str, str] = {}

#     def get_default_select(self, obj: BaseQueryModel):


#         def _get_default_select():
#         for key_name in self.__dir__():
#             obj: field.QueryField = getattr(self, key_name)
#             if isinstance(obj, field.QueryField):
#                 if obj.name is None:
#                     obj.name = key_name

#                 self.key[key_name] = obj

#                 if not obj.is_hidden:
#                     self.default_select.add(obj.name)
#                 if obj.is_identifier:
#                     self.identifier = key_name
