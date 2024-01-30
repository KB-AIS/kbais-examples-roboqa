import tomllib

from abc import ABC, abstractmethod
from functools import reduce
from typing import Optional, Dict, TypeVar, List

CONFIG_NAME_DEFAULT = "config"

T = TypeVar('T')


class AppConfig(ABC):
    @abstractmethod
    def get_value(self, section: List[str]) -> Optional[T]:
        pass


class TomlAppConfig(AppConfig):
    _EXTENSION = ".toml"

    def __init__(self, config_name: Optional[str] = None) -> None:
        self.config_name = (CONFIG_NAME_DEFAULT, config_name)[type(config_name) is str]
        self.config_vals: Optional[Dict] = None

    def get_value(self, section: List[str]) -> Optional[T]:
        if self.config_vals is None:
            self._load()

        return reduce(lambda d, key: d.get(key), section, self.config_vals)

    def _load(self) -> None:
        has_extension = self.config_name.lower().endswith(self._EXTENSION)

        config_file_path = f"{self.config_name}{(self._EXTENSION, '')[has_extension]}"

        with open(config_file_path, "rb") as config_file:
            self.config_vals = tomllib.load(config_file)
