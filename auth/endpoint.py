import random
from datetime import datetime
from sanic.request import Request

from auth.auth import user_auth
from base import ResponseHandler
from base.exceptions import (
    BadRequestException,
    ForbiddenException,
    NotFoundException,
    UnauthorizedException,
)
from base.tracking import generate_tracking_data
from connector.gino import get_bind
from notification.notifier import EmailNotifier
from .cfg import logger
from .datadef import (
    AuthUserData,
    ChangePasswordData,
    LoginData,
    ResetPasswordConfirm,
    ResetPasswordRequest,
    ResetPasswordRequestData,
    UserData,
    UserInfo,
)
from .model import DefaultModel, UserAuthModel, UserRequestModel, db


@ResponseHandler.handler
async def register(request: Request):
    data = UserInfo.create(request.json)
    user_data = UserData.extend_pclass(data)

    await get_bind()
    async with db.transaction():
        user = (
            await DefaultModel["user"]
            .query.where(
                db.or_(
                    DefaultModel["user"].username == user_data.username,
                    DefaultModel["user"].contact__email == user_data.contact__email,
                )
            )
            .gino.first()
        )
        if user is not None:
            if user.username == user_data.username:
                raise ForbiddenException(errcode=403801, message="Username is existed!")
            else:
                raise ForbiddenException(
                    errcode=403805, message="Email address is existed!"
                )
        await DefaultModel["user"].create(
            **user_data.serialize(), **generate_tracking_data(user_data._id)
        )
        login_data = AuthUserData.extend_pclass(data, user_id=user_data._id)
        await UserAuthModel.create(**login_data.serialize())
        return {"user_id": data._id, "key": login_data.auth_key}


@ResponseHandler.handler
async def login(request: Request):
    login_data = LoginData.create(request.json)
    logger.info("user %r is logging" % login_data.username)

    await get_bind()
    async with db.transaction():
        user = (
            await DefaultModel["user"]
            .query.where(
                db.and_(
                    DefaultModel["user"].username == login_data.username,
                    DefaultModel["user"].password == login_data.password,
                )
            )
            .gino.first()
        )
        if user is None:
            raise UnauthorizedException(
                errcode=401802, message="Username or password is incorrect!"
            )
        auth_user_data = AuthUserData.extend_pclass(login_data, user_id=user._id)
        await UserAuthModel.create(**auth_user_data.serialize())
        return {"user_id": user._id, "key": auth_user_data.auth_key}


@ResponseHandler.handler
@user_auth
async def logout(request: Request, user: UserInfo):
    await get_bind()
    async with db.transaction():
        status, _ = await UserAuthModel.delete.where(
            UserAuthModel.auth_key == user.auth_key,
        ).gino.status()
        if status == "DELETE 1":
            return {"message": "SUCCESS"}
        else:
            return {"message": "FAIL", "status": status}


@ResponseHandler.handler
@user_auth
async def change_password(request: Request, user: UserInfo):
    pass_data: ChangePasswordData = ChangePasswordData.create(request.json)
    if user.password != pass_data.current_password:
        raise BadRequestException(errcode=400022, message="Wrong password!")

    await get_bind()
    async with db.transaction():
        status, _ = (
            await DefaultModel["user"]
            .update.values(password=pass_data.new_password)
            .where(
                db.and_(
                    DefaultModel["user"]._id == user._id,
                    DefaultModel["user"]._etag == user._etag,
                )
            )
            .gino.status()
        )
        if status == "UPDATE 1":
            return {"message": "SUCCESS"}
        else:
            return {"message": "FAIL", "status": status}


@ResponseHandler.handler
async def reset_password_request(request: Request):
    data: ResetPasswordRequest = ResetPasswordRequest.create(request.json)

    await get_bind()
    async with db.transaction():
        user = (
            await DefaultModel["user"]
            .query.where(
                db.and_(
                    DefaultModel["user"].contact__email == data.email,
                    DefaultModel["user"].is_activate == True,
                )
            )
            .gino.first()
        )
        if user is None:
            raise NotFoundException(errcode=404023, message="User is not found!")

        random.seed(datetime.now())
        code = "".join([str(random.randrange(0, 9)) for i in range(0, 6)])
        request_data = ResetPasswordRequestData(
            user_id=user._id, code=code, request_type="P"
        )

        await UserRequestModel.create(**request_data.serialize())
        email_message = (
            f"Hi {user.fullname}.<br>"
            "To comfirm you reset password request. "
            f"Here is your code: {code} <br>"
            "Thank you."
        )
        EmailNotifier.send_smtp_email(
            [data.email], "Reset password request", email_message
        )


@ResponseHandler.handler
async def confirm_reset_password_request(request: Request):
    data: ResetPasswordConfirm = ResetPasswordConfirm.create(request.json)

    await get_bind()
    async with db.transaction():
        user_request: UserRequestModel = (
            await UserRequestModel.join(DefaultModel["user"])
            .select()
            .where(
                db.and_(
                    DefaultModel["user"].contact__email == data.email,
                    UserRequestModel.code == data.code,
                )
            )
            .gino.first()
        )
        if user_request is None:
            raise BadRequestException(
                errcode=400806, message="Your email or code is incorrect!"
            )
    if user_request.expiration_date < datetime.utcnow():
        await UserRequestModel.delete.where(
            db.and_(
                UserRequestModel.user_id == user_request.user_id,
                UserRequestModel.code == user_request.code,
            )
        ).gino.status()
        raise BadRequestException(errcode=400807, message="Your request is expired!")

    async with db.transaction():
        auth_user_data = AuthUserData.extend_pclass(data, user_id=user_request.user_id)
        await UserAuthModel.create(**auth_user_data.serialize())
        await UserRequestModel.delete.where(
            db.and_(
                UserRequestModel.user_id == user_request.user_id,
                UserRequestModel.code == user_request.code,
            )
        ).gino.status()
        return {"user_id": user_request.user_id, "key": auth_user_data.auth_key}
