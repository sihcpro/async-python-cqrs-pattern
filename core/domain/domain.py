from auth.auth import user_auth
from auth.datadef import UserInfo
from base.identifier import UUID_GENR
from base.response_handler import ResponseHandler

from ..cfg import logger
from ..datadef import Initiator
from .domain_process import DomainProcess


class Domain(DomainProcess):
    @classmethod
    def register_domain_endpoint(cls, app):
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
            data = request.json

            initiator = Initiator(
                resource=resource,
                identifier=(UUID_GENR() if identifier is None else identifier),
            )
            domain = cls(user=user, initiator=initiator)

            domain.process_command(entity_name=command, data=data)
            responses = await domain.commit()
            logger.debug("~~~~~~~~>>>>>>> Done request <<<<<<<~~~~~~~~")
            if len(responses) > 0:
                return await responses[-1].execute()

        app.add_route(_command_ingress, resource_path, methods=["POST"])
        app.add_route(
            _command_ingress, item_path, methods=["POST", "PUT", "PATCH", "DELETE"],
        )
