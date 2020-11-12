from .response import AppResponse
from app.cfg import logger


class AppException(Exception):
    __status_code__ = 500
    __message__ = "Application Error"
    __debug_info__ = True

    def __init__(self, errcode: int, message: str = None, data: dict = None):
        self.errcode = errcode
        self.data = data if data is not None else dict()
        self.message = message or self.__message__

        super(AppException, self).__init__(self.message)
        self.resp: AppResponse = AppResponse(
            body=self.build_body(), status=self.__status_code__
        )
        self.notify()

    def notify(self):
        if not self.__debug_info__:
            return
        logger.error("[%d] %s\n%r", self.errcode, self.message, self.data)
        logger.exception(self)

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
    __debug_info__ = False


class ForbiddenException(AppException):
    __status_code__ = 403
    __message__ = "Forbidden"


class NotFoundException(AppException):
    __status_code__ = 404
    __message__ = "Not found item"
    __debug_info__ = False
