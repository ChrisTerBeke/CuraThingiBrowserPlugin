import json
from json import JSONDecodeError
from typing import Dict

from PyQt5.QtCore import QObject


class JSONObject(QObject):
    """ Simple class that converts a JSON object to a Python model. """
    def __init__(self, _dict: Dict[str, any]):
        if _dict:
            vars(self).update(_dict)
        super().__init__()