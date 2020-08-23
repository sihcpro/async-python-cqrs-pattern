from .state_connector import StateConnector
from .state_register import StateRegister


class StateMgr(StateConnector, StateRegister):
    pass
