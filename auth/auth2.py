import re
from sanic.request import Request
from sqlalchemy.sql.expression import select

from base.exceptions import UnauthorizedException
from base.model import db
from base.ssl import default_ssl
from connector.cfg import config as connector_cfg
from connector.gino import db as gino_db
from connector.gino import get_async_connection, get_bind, get_connection
from .cfg import logger
from .datadef import UserInfo
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
            # async with gino_db.with_bind(connector_cfg.DB_DSN, ssl=default_ssl()):
            # async with gino_db.with_bind(await get_bind()):
            await get_bind()
            result = await (
                db.select(
                    [
                        UserModel,
                        UserAuthModel.auth_key,
                        UserAuthModel.device,
                        UserAuthModel.location,
                        UserAuthModel.information,
                    ]
                )
                .select_from(UserModel.join(UserAuthModel))
                .where(UserAuthModel.auth_key == auth_key)
                .gino.first()
            )
            # conn = await get_async_connection()
            # result = await (
            #     conn.execute(
            #         select(
            #             [
            #                 UserModel,
            #                 UserAuthModel.auth_key,
            #                 UserAuthModel.device,
            #                 UserAuthModel.location,
            #                 UserAuthModel.information,
            #             ]
            #         )
            #         .where(
            #             db.and_(
            #                 UserModel._id == UserAuthModel.user_id,
            #                 UserAuthModel.auth_key == auth_key,
            #             )
            #         )
            #         .limit(1)
            #         .execute()
            #     )
            # )
            # result = await (
            #     UserModel.join(UserAuthModel)
            #     .select(
            #         [
            #             UserModel,
            #             UserAuthModel.auth_key,
            #             UserAuthModel.device,
            #             UserAuthModel.location,
            #             UserAuthModel.information,
            #         ]
            #     )
            #     .gino.first()
            # )
            user_data = {key: value for key, value in result.items()}
            print("--------> user_data", user_data)
            user: UserInfo = UserInfo.create(user_data, ignore_extra=True)
            if user is None:
                raise UnauthorizedException(errcode=401803)
            logger.debug(
                "User '%r' with key '%s' logged in" % (user.username, auth_key)
            )
            return await func(request, user, *args, **kwargs)
        else:
            raise UnauthorizedException(errcode=401804)

    return check_auth
