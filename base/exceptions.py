from builtins import isinstance
from pyrsistent import _checked_types

from .response import AppResponse

try:
    # Follow log level of the app
    from app.cfg import logger
except Exception:
    from .cfg import logger


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


class ExceptionHandler:
    @classmethod
    def handle_common_exception(cls, error: Exception):
        if isinstance(error, AttributeError):
            return BadRequestException(
                errcode=400906, message=f"Missing field {str(error)}"
            ).resp
        elif isinstance(error, _checked_types.InvariantException):
            if error.missing_fields:
                return BadRequestException(
                    errcode=400907, message=f"Missing field {error.missing_fields[0]}"
                ).resp
            else:
                return BadRequestException(
                    errcode=400908, message="Something went wrong", data=error.__dict__
                ).resp

        return AppException(errcode=500902, message=str(error)).resp

    @classmethod
    def handler(cls, error):
        if isinstance(error, AppException):
            return error.resp
        else:
            return cls.handle_common_exception(error)
