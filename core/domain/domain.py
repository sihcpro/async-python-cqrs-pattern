from sanic import Sanic

from .domain_request import DomainRequest


class Domain(DomainRequest):
    app: Sanic
