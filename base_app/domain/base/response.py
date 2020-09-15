from core import JsonResponse
from pyrsistent import field

from .domain import BaseDomain


@BaseDomain.register_entity
class BaseGenericResponse(JsonResponse):
    data = field(dict)


@BaseDomain.response_handler(BaseGenericResponse)
async def generic_response(data: dict):
    return data
