from sanic.request import Request

from base.exceptions import UnauthorizedException

from .cfg import logger
from .model import UserAuthModel, UserModel


def user_auth(func):
    async def check_auth(request: Request, *args, **kwargs):
        auth_header = request.headers.get("authorization", "")
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
