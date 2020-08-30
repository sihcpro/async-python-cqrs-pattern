from sanic.response import BaseHTTPResponse

from .cfg import logger
from .exceptions import AppException
from .response import AppResponse, json_dumps


class AppErrorResponse(AppResponse):
    def __init__(
        self, error: AppException = None, dumps=json_dumps, **kwargs,
    ):
        if error is None:
            error = AppException(errcode=500999)
        body = dumps(error.build_body(), **kwargs)
        super(AppResponse, self).__init__(
            body=body,
            status=error.__status_code__,
            headers=self.headers,
            content_type=self.content_type,
        )


class ResponseHandler(AppResponse):
    @classmethod
    def handler(cls, func):
        async def _handler(*args, **kwargs):
            try:
                resp = await func(*args, **kwargs)
                if isinstance(resp, BaseHTTPResponse):
                    return resp
                elif isinstance(resp, dict):
                    return AppResponse(data=resp)
                else:
                    return AppResponse()
            except AppException as app_ex:
                logger.exception(app_ex)
                return AppErrorResponse(error=app_ex)
            except Exception as sys_ex:
                logger.exception(sys_ex)
                app_ex = AppException(errcode=500902, message=str(sys_ex))
                return AppErrorResponse(error=app_ex)

        return _handler
