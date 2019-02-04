# Copyright (c) 2018 Chris ter Beke.
# Thingiverse plugin is released under the terms of the LGPLv3 or higher.
from typing import List

from PyQt5.QtCore import QObject, pyqtProperty, pyqtSignal, pyqtSlot

from .Thing import Thing
from .ThingiverseApiClient import ThingiverseApiClient


class ThingiverseService(QObject):
    """
    The ThingiverseService uses the API client to serve thingiverse content to the UI.
    """
    
    # Signal triggered when new things are found.
    thingsChanged = pyqtSignal()
    
    def __init__(self, parent = None):
        super().__init__(parent)
        
        # Holds the things found in search results.
        self._things = []  # type: List[Thing]

        # The API client that we do all calls to Thingiverse with.
        self._api_client = ThingiverseApiClient()  # type: ThingiverseApiClient

    @pyqtProperty("QVariantList", notify = thingsChanged)
    def things(self) -> List[Thing]:
        """
        Get a list of found things. Updated when performing a search.
        :return: The things.
        """
        return self._things
    
    @pyqtSlot(str, name = "download")
    def download(self, thing_id: int) -> None:
        """
        Download and load a thing by it's ID.
        The downloaded object will be placed on the build plate.
        :param thing_id: The ID of the thing.
        """
        self._api_client.download(thing_id, self._onDownloadFinished)
        
    def _onDownloadFinished(self, thing_bytes: bytes) -> None:
        print("thing_bytes", thing_bytes)

    @pyqtSlot(str, name = "search")
    def search(self, search_terms: str) -> None:
        """
        Search for things by search terms.
        The search is done async and the result will be populated in self._things.
        :param search_terms: The search terms separated by a space.
        """
        self._api_client.search(search_terms, self._onSearchFinished)
        
    def _onSearchFinished(self, things: List[Thing]) -> None:
        """
        Callback for receiving search results on.
        :param things: The found things.
        """
        self._things = things
        self.thingsChanged.emit()
