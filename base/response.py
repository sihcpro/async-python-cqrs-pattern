from json import dumps

from sanic.response import HTTPResponse

from .encoder import CustomEncoder


def json_dumps(body, **kwargs):
    return dumps(body, cls=CustomEncoder, **kwargs)


class AppResponse(HTTPResponse):
    CONTENT_TYPE = "application/json"
    HEADERS = {}
    DUMP = json_dumps
    STATUS = 200

    def __init__(
        self,
        body: dict = None,
        data: dict = None,
        meta: dict = None,
        status: int = STATUS,
        body_bytes: str = b"",
        dumps=DUMP,
        headers: dict = HEADERS,
        **kwargs,
    ):
        if body is None:
            _data = data if data is not None else {}
            body = {
                "status": 200,
                "data": {"items": _data, "meta": meta or {}},
                "messsage": "OK",
            }
        body = dumps(body, **kwargs)
        super().__init__(
            body=body,
            status=status,
            headers=headers,
            content_type=self.CONTENT_TYPE,
            body_bytes=body_bytes,
        )
