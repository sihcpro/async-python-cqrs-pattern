from sanic import Sanic


class BaseDomain:
    __namespace__ = "base"
    app: Sanic

    @property
    def namespace(self):
        return self.__namespace__
