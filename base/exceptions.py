from .response import AppResponse


class AppException(Exception):
    __status_code__ = 500
    __message__ = "Application Error"

    def __init__(self, errcode: int, message: str = None, data: dict = None):
        self.errcode = errcode
        self.data = data if data is not None else dict()
        self.message = message or self.__message__
        self.resp = AppResponse(body=self.build_body(), status=self.__status_code__)

        super(AppException, self).__init__(self.message)

    def build_body(self) -> dict:
        return {
            "status": self.__status_code__,
            "errcode": self.errcode,
            "data-error": self.data,
            "message": self.message,
        }


class BadRequestException(AppException):
    __status_code__ = 400
    __message__ = "Bad request"


class UnauthorizedException(AppException):
    __status_code__ = 401
    __message__ = "UnauthorizedException"


class ForbiddenException(AppException):
    __status_code__ = 403
    __message__ = "Forbidden"


class NotFoundException(AppException):
    __status_code__ = 404
    __message__ = "Not found item"
