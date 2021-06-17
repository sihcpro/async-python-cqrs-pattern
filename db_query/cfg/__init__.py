from system import load_app
from . import defaults

config: defaults
config, logger = load_app(__name__)
