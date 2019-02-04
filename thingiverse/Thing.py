# Copyright (c) 2018 Chris ter Beke.
# Thingiverse plugin is released under the terms of the LGPLv3 or higher.
from PyQt5.QtCore import QObject, pyqtProperty


class Thing(QObject):
    
    def __init__(self,
                 id: str,
                 name: str,
                 url: str,
                 public_url: str,
                 thumbnail: str,
                 creator: dict,
                 is_private: bool,
                 is_purchased: bool,
                 is_published: bool
                 ) -> None:
        super().__init__()
        self._id = id  # type: int
        self._name = name  # type: str
        self._url = url  # type: str
        self._public_url = public_url  # type: str
        self._thumbnail = thumbnail  # type: str

    @pyqtProperty(int, constant = True)
    def thingId(self) -> int:
        return self._id
        
    @pyqtProperty(str, constant = True)
    def name(self) -> str:
        return self._name

    @pyqtProperty(str, constant = True)
    def thumbnail_url(self) -> str:
        return self._thumbnail
