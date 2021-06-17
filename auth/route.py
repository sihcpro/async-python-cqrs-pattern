from sanic.request import Request
from sanic.response import json

from base.sanic import SanicApp
from .endpoint import (
    change_password,
    confirm_reset_password_request,
    login,
    logout,
    register,
    reset_password_request,
)


def config_auth_route(app: SanicApp):
    async def home_page(request: Request):
        return json({"hello": "world"})

    app.add_route(home_page, "/", methods=["GET"])
    app.add_route(login, "/login", methods=["POST"])
    app.add_route(register, "/register", methods=["POST"])
    app.add_route(logout, "/logout", methods=["POST"])
    app.add_route(change_password, "/change-password", methods=["POST"])
    app.add_route(reset_password_request, "/reset-password-request", methods=["POST"])
    app.add_route(
        confirm_reset_password_request,
        "/confirm-reset-password-request",
        methods=["POST"],
    )
