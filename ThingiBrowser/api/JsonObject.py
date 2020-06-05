# Copyright (c) 2020.
# ThingiBrowser plugin is released under the terms of the LGPLv3 or higher.
from typing import Dict, Any

from PyQt5.QtCore import QObject


class JsonObject(QObject):
    """ Simple class that converts a JSON object to a Python model. """
    def __init__(self, _dict: Dict[str, Any]):
        self.type = self.__class__.__name__
        if _dict:
            vars(self).update(_dict)
        super().__init__()

    def toStruct(self) -> Dict[str, Any]:
        """
        Get a dict representation of the object.
        :return: The dict.
        """
        return self.__dict__


class ApiError(JsonObject):
    """ Class representing an API error. """
    def __init__(self, _dict: Dict[str, Any]):
        self.error = None
        super().__init__(_dict)


class Thing(JsonObject):
    """ Class representing a thing. """
    def __init__(self, _dict: Dict[str, Any]):
        self.id = None
        self.thumbnail = None
        self.name = None
        self.url = None
        self.description = None
        super().__init__(_dict)


class Collection(JsonObject):
    """ Class representing a collection. """
    def __init__(self, _dict: Dict[str, Any]):
        self.id = None
        self.thumbnail = None
        self.name = None
        self.url = None
        self.description = None
        super().__init__(_dict)


class ThingFile(JsonObject):
    """ Class representing a thing file. """
    def __init__(self, _dict: Dict[str, Any]):
        self.id = None
        self.thumbnail = None
        self.name = None
        self.url = None
        super().__init__(_dict)


class UserData(JsonObject):
    """ Class representing user data. """
    def __init__(self, _dict: Dict[str, Any]):
        self.username = None
        super().__init__(_dict)
