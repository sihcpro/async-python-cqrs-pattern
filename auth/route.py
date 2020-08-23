from sanic.request import Request
from sanic.response import json

from .endpoint import login, register


def config_auth_route(app):
    @app.route("/")
    async def home_page(request: Request):
        return json({"hello": "world"})

    app.add_route(login, "/login", methods=["POST"])
    app.add_route(register, "/register", methods=["POST"])
