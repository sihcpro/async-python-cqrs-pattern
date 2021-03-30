from ..generic import GenericResponse, generic_response
from .domain_request import DomainRequest


class Domain(DomainRequest):
    @classmethod
    def register_generic_response(cls):
        cls.register_entity(GenericResponse)
        cls.response_handler(GenericResponse)(generic_response)

    @classmethod
    def register_generic_function(cls):
        cls.register_generic_response()
