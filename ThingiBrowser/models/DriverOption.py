# Copyright (c) 2020.
# Thingiverse plugin is released under the terms of the LGPLv3 or higher.
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..api.AbstractApiClient import AbstractApiClient


class DriverOption:

    def __init__(self, label: str, driver: "AbstractApiClient") -> None:
        self._label = label
        self._driver = driver

    @property
    def label(self) -> str:
        return self._label

    @property
    def driver(self) -> "AbstractApiClient":
        return self._driver
