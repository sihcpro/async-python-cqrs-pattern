from functools import wraps

from ..command import Command
from ..entity import Entity
from ..cfg import logger
from ..response import BaseResponse
from ..event import Event
from . import BaseDomain


class DomainHandler(BaseDomain):
    __handler__ = {}

    @property
    def handler(self):
        return self.__handler__

    @classmethod
    def command_handler(cls, *entities: Entity):
        @wraps(entities)
        def _set_command(func):
            logger.debug(
                "%s '%s' %s '%s'" % ("Reg", cls.__namespace__, "Comm", func.__name__)
            )
            if len(entities) < 1:
                raise ValueError("A command handler must has at least one entity")
            for entity in entities:
                cls.__handler__[(cls.__namespace__, Command, entity)] = func
            return func

        return _set_command

    @classmethod
    def lookup_command_handler(cls, entity: Entity):
        key = (cls.__namespace__, Command, entity)
        return cls.__handler__[key]

    @classmethod
    def response_handler(cls, *entities: Entity):
        @wraps(entities)
        def _set_response(func):
            logger.debug(
                "%s '%s' %s '%s'" % ("Reg", cls.__namespace__, "Resp", func.__name__)
            )
            if len(entities) < 1:
                raise ValueError("A command handler must has at least one entity")
            for entity in entities:
                cls.__handler__[(cls.__namespace__, BaseResponse, entity)] = func

        return _set_response

    @classmethod
    def lookup_response_handler(cls, entity: Entity):
        key = (cls.__namespace__, BaseResponse, entity)
        return cls.__handler__[key]

    @classmethod
    def event_handler(cls, *entities: Entity):
        @wraps(entities)
        def _set_event(func):
            logger.debug(
                "%s '%s' %s '%s'" % ("Reg", cls.__namespace__, "Even", func.__name__)
            )
            if len(entities) < 1:
                raise ValueError("A command handler must has at least one entity")
            for entity in entities:
                cls.__handler__[(cls.__namespace__, Event, entity)] = func

        return _set_event

    @classmethod
    def lookup_event_handler(cls, entity: Entity):
        key = (cls.__namespace__, Event, entity)
        return cls.__handler__[key]
