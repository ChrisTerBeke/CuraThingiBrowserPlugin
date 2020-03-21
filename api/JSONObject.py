from typing import Optional, Dict, List, Any
import json
from json import JSONDecodeError
from PyQt5.QtCore import QObject

class JSONObject(QObject):
    """ Simple class that converts a JSON object to a Python model. """
    def __init__(self, _dict: Dict[str, Any]):
        if _dict:
            vars(self).update(_dict)
        super().__init__()

class BaseModel(JSONObject):
    URL = None # type: str
    ID = None # type: str
    NAME = None # type: str

class Thing(BaseModel):
    DESCRIPTION = None # type: Optional[str]
    THUMBNAIL = None # type: Optional[str]

class ThingFile(BaseModel):
    THUMBNAIL = None # type: Optional[str]