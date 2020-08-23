from base.model import db
from .cfg import logger


def config_connector(app):
    logger.info("Init Connector")
    db.init_app(app)
