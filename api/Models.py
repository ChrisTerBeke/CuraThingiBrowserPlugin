from typing import Optional, Dict, List, Any
from .JSONObject import JSONObject

class BaseModel(JSONObject):
    URL = None # type: str
    ID = None # type: str
    NAME = None # type: str

class Thing(BaseModel):
    DESCRIPTION = None # type: Optional[str]
    THUMBNAIL = None # type: Optional[str]

class ThingFile(BaseModel):
    THUMBNAIL = None # type: Optional[str]