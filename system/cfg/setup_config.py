import importlib.util
import re
from os import path

from .helper import type_parse


class Config:
    __module_config__ = {}

    regex_python_args = re.compile(r"--([A-Za-z_]*)=(\w+)")

    def __init__(self, module):
        self.__module__ = module
        self.__module_name__ = module.split(".")[0]
        sysdefault = self.__module_config__.get("system", None)
        self.__config__ = sysdefault.__config__ if sysdefault else {}
        self.__config__ = self.load_module(
            f"{self.__module__}.defaults", update_only=False,
        )
        self.__module_config__[self.__module_name__] = self

    def update_config(self, config: dict, update_only=True):
        if update_only:
            config = {
                key: value
                for key, value in config.items()
                if key in self.__config__
            }
        self.__config__.update(config)

    def prepare_config(self, file_config) -> dict:
        config = {}
        for key, value in file_config.__dict__.items():
            key_upper = key.upper()
            config[key_upper] = value
        return config

    def load_file(self, file_path, update_only=True):
        spec = importlib.util.spec_from_file_location(
            self.__module__, file_path
        )
        file_config = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(file_config)

        config = self.prepare_config(file_config)
        self.update_config(config, update_only)
        return self.__config__

    def load_module(self, module_path, update_only=True):
        file_config = importlib.import_module(module_path)

        config = self.prepare_config(file_config)
        self.update_config(config, update_only)
        return self.__config__

    def load_environment(self, environment: str):
        file_path = f"./env/{environment}/config.py"
        return self.load_file(file_path)

    def load_argument(self, args: list):
        for arg in args:
            match = self.regex_python_args.search(arg)
            if not match:
                continue
            key = match.group(1).upper()
            value = match.group(2)
            if key in self.__config__:
                old_value = self.__config__[key]
                new_value = type_parse(type(old_value), value)
                self.__config__.update({key: new_value})

    def items(self):
        return self.__config__.items()

    def __getattr__(self, value):
        return self.__config__[value]

    @classmethod
    def get_module_config(cls, module_name):
        return cls.__module_config__[module_name]
