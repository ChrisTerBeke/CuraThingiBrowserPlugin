# Copyright (c) 2020.
# Thingiverse plugin is released under the terms of the LGPLv3 or higher.
from typing import Callable


class ViewOption:

    def __init__(self, label: str, query: Callable[[], None]) -> None:
        self._label = label
        self._query = query

    @property
    def label(self) -> str:
        return self._label

    @property
    def query(self) -> Callable[[], None]:
        return self._query
