from sanic.request import Request

from base import ResponseHandler
from base.exceptions import ForbiddenException, UnauthorizedException
from base.tracking import generate_tracking_data
from connector.gino import get_bind
from .cfg import logger
from .datadef import AuthUserData, LoginData, UserData, UserInfo
from .model import UserAuthModel, UserModel, db


@ResponseHandler.handler
async def register(request: Request):
    await get_bind()
    async with db.transaction():
        data = UserInfo.create(request.json)
        user_data = UserData.extend_pclass(data)
        user = await UserModel.query.where(
            db.or_(
                UserModel.username == user_data.username,
                UserModel.contact__email == user_data.contact__email,
            )
        ).gino.first()
        if user is not None:
            if user.username == user_data.username:
                raise ForbiddenException(errcode=403801, message="Username is existed!")
            else:
                raise ForbiddenException(
                    errcode=403805, message="Email address is existed!"
                )
        await UserModel.create(
            **user_data.serialize(), **generate_tracking_data(user_data._id)
        )
        login_data = AuthUserData.extend_pclass(data, user_id=user_data._id)
        await UserAuthModel.create(**login_data.serialize())
        return {"user_id": data._id, "key": login_data.auth_key}


@ResponseHandler.handler
async def login(request: Request):
    await get_bind()
    async with db.transaction():
        login_data = LoginData.create(request.json)

        logger.info("user %r is logging" % login_data.username)
        user = await UserModel.query.where(
            db.and_(
                UserModel.username == login_data.username,
                UserModel.password == login_data.password,
            )
        ).gino.first()
        if user is None:
            raise UnauthorizedException(
                errcode=401802, message="Username or password is incorrect!"
            )
        auth_user_data = AuthUserData.extend_pclass(login_data, user_id=user._id)
        await UserAuthModel.create(**auth_user_data.serialize())
        return {"user_id": user._id, "key": auth_user_data.auth_key}
