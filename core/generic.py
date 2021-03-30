from pyrsistent import field

from base.type import nullable
from .response import JsonResponse


class GenericResponse(JsonResponse):
    data = field(nullable(dict))


async def generic_response(data: dict):
    return data
