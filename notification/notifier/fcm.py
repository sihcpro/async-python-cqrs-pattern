from pyfcm import FCMNotification

from base.encoder import CustomEncoder
from ..base.notifier import Notifier
from ..cfg import config


class FCMNotifier(Notifier):
    def __init__(self):
        self.notifier = FCMNotification(
            config.FCM_SERVER_KEY, env=config.ENV, json_encoder=CustomEncoder
        )
