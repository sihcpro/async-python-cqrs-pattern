from sanic.request import Request


class AuthRequest(Request):
    def add_authentication_info(self):
        pass
