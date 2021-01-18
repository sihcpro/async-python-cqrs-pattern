import re
from sanic.request import Request

from base.exceptions import UnauthorizedException
from .cfg import logger
from .model import UserAuthModel, UserModel


def user_auth(func):
    cookie_re = re.compile(r"(\w*)=([^;]*)")
    auth_keyword = "authorization"

    def get_cookie(cookie):
        if isinstance(cookie, dict):
            return cookie.get(auth_keyword, "")
        for match_cookie in cookie_re.findall(cookie):
            if match_cookie[0] == auth_keyword:
                return match_cookie[1]
        return ""

    async def check_auth(request: Request, *args, **kwargs):
        auth_header = request.headers.get(auth_keyword, "") or get_cookie(
            request.headers.get("cookie", {})
        )
        if auth_header.startswith("Bearer"):
            auth_key = auth_header[7:]
            user = (
                await UserModel.query.select_from(UserModel.join(UserAuthModel))
                .where(UserAuthModel.auth_key == auth_key)
                .gino.first()
            )
            if user is None:
                raise UnauthorizedException(errcode=401803)
            logger.debug(
                "User '%r' with key '%s' logged in" % (user.username, auth_key)
            )
            return await func(request, user, *args, **kwargs)
        else:
            raise UnauthorizedException(errcode=401804)

    return check_auth
