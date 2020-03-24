# Copyright (c) 2020 Chris ter Beke.
# Thingiverse plugin is released under the terms of the LGPLv3 or higher.
from typing import Dict, Any
from PyQt5.QtCore import QObject


class JsonObject(QObject):
    """ Simple class that converts a JSON object to a Python model. """
    def __init__(self, _dict: Dict[str, Any]):
        self.type = self.__class__.__name__
        if _dict:
            vars(self).update(_dict)
        super().__init__()


class Thing(JsonObject):
    """ Class representing a thing. """
    id = None
    thumbnail = None
    name = None
    url = None
    description = None


class Collection(JsonObject):
    """ Class representing a collection. """
    id = None
    thumbnail = None
    name = None
    url = None
    description = None


class ThingFile(JsonObject):
    """ Class representing a thing file. """
    id = None
    thumbnail = None
    name = None
    url = None
