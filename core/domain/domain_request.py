from auth.auth import user_auth
from auth.datadef import UserInfo
from base.exceptions import BadRequestException
from base.identifier import UUID_GENR
from base.response_handler import ResponseHandler
from ..cfg import logger
from ..datadef import Initiator
from .domain_process import DomainProcess


class DomainRequest(DomainProcess):
    @classmethod
    def handle_request_data(cls, request):
        content_type = request.headers["content-type"]
        if content_type.startswith("application/json"):
            return request.json
        elif content_type.startswith("multipart/form-data") or content_type.startswith(
            "application/x-www-form-urlencoded"
        ):
            data = {}
            data.update(request.files)
            data.update(request.form)
            try:
                data.update(request.json)
            except Exception:
                pass
            return data
        else:
            raise BadRequestException(
                errcode=400905, message=f"Content type '{content_type}' is not allowed!"
            )

    @classmethod
    def register_domain_endpoint(cls):
        logger.debug("%s '%s' %s" % ("Reg", cls.__namespace__, "Domain"))

        resource_path = (
            rf"/{cls.__namespace__}:<command:[A-z0-9\-_]*>" r"/<resource:[A-z0-9\-_]*>"
        )
        item_path = rf"{resource_path}/<identifier:[0-9A-Fa-f\-_]*>"

        @ResponseHandler.handler
        @user_auth
        async def _command_ingress(
            request, user: UserInfo, command, resource, identifier=None
        ):
            logger.debug(
                ">>>>>>> Command '%s' to %r <<<<<<<<"
                % (command, (cls.__namespace__, resource, identifier))
            )
            data = cls.handle_request_data(request)

            initiator = Initiator(
                resource=resource,
                identifier=(UUID_GENR() if identifier is None else identifier),
            )
            domain: DomainProcess = cls(user=user, initiator=initiator)

            domain.process_command(entity_name=command, data=data)
            responses = await domain.commit()
            logger.debug("~~~~~~~~>>>>>>> Done request <<<<<<<~~~~~~~~")
            if len(responses) > 0:
                return await responses[-1].execute()

        cls.app.add_route(_command_ingress, resource_path, methods=["POST"])
        cls.app.add_route(
            _command_ingress, item_path, methods=["POST", "PUT", "PATCH", "DELETE"]
        )

    @classmethod
    def register_custom_domain_endpoint(
        cls,
        route: str,
        resource: str,
        auth_handler=user_auth,
        resp_handler=ResponseHandler.handler,
        methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    ):
        def register_endpoint(func):
            endpoint = f"/{cls.__namespace__}/{route}"
            logger.debug("Reg '%s' Endp '%s'" % (cls.__namespace__, route))

            @resp_handler
            @auth_handler
            async def _command_ingress(request, *args, **kwargs):
                logger.debug(
                    ">>>>>>> Request '%s' to %r <<<<<<<<"
                    % (route, (cls.__namespace__, str(func)))
                )

                data = (
                    cls.handle_request_data(request)
                    if request.method != "GET"
                    else None
                )

                identifier = kwargs.get("identifier", None)
                initiator = Initiator(
                    resource=resource,
                    identifier=(UUID_GENR() if identifier is None else identifier),
                )
                user = None
                if auth_handler is user_auth:
                    user = args[0]
                    args = args[1:]
                domain: DomainProcess = cls(
                    user=user,
                    initiator=initiator,
                )

                resp = await func(
                    domain.proxy, domain.context, data, request, *args, **kwargs
                )
                logger.debug("~~~~~~~~>>>>>>> Done request <<<<<<<~~~~~~~~")
                return resp

            cls.app.add_route(_command_ingress, endpoint, methods=methods)

        return register_endpoint
