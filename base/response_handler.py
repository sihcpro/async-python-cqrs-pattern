from sanic.response import BaseHTTPResponse

from .exceptions import AppException
from .response import AppResponse


class ResponseHandler(AppResponse):
    @classmethod
    def response_handler(cls, resp):
        if isinstance(resp, BaseHTTPResponse):
            return resp
        elif isinstance(resp, dict):
            return AppResponse(data=resp)
        else:
            return AppResponse()

    @classmethod
    def exception_handler(cls, error):
        if isinstance(error, AppException):
            return error.resp
        else:
            return AppException(errcode=500902, message=str(error)).resp

    @classmethod
    def handler(cls, func):
        async def _handler(*args, **kwargs):
            try:
                resp = await func(*args, **kwargs)
                return cls.response_handler(resp)
            except Exception as e:
                return cls.exception_handler(e)

        return _handler
