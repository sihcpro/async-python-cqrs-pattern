import logging
import sys

from .setup_config import Config
from .setup_logger import setup_logger


def load_app(name: str) -> (Config, logging):
    config = Config(name)
    config.load_argument(sys.argv)
    config.load_environment(config.ENV)
    config.load_argument(sys.argv)

    logger = setup_logger(
        module_name=config.__module_name__, log_config=config
    )
    return config, logger


config, logger = load_app(__name__)

__all__ = ("config", "logger", "load_app")
