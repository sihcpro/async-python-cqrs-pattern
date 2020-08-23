from json import dumps

from sanic.response import HTTPResponse

from .encoder import CustomEncoder


def json_dumps(body, **kwargs):
    return dumps(body, cls=CustomEncoder, **kwargs)


class AppResponse(HTTPResponse):
    content_type = "application/json"
    headers = ""

    def __init__(
        self,
        body: dict = None,
        data: dict = None,
        status: int = 200,
        body_bytes: str = b"",
        dumps=json_dumps,
        **kwargs,
    ):
        if body is None:
            _data = data or {}
            body = {"status": 200, "data": _data, "messsage": "OK"}
        body = dumps(body, **kwargs)
        super().__init__(
            body=body,
            status=status,
            headers=self.headers,
            content_type=self.content_type,
            body_bytes=body_bytes,
        )
