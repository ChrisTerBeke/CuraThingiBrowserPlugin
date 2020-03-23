# Copyright (c) 2020 Chris ter Beke.
# Thingiverse plugin is released under the terms of the LGPLv3 or higher.
from typing import List, Callable, Any, Optional

from PyQt5.QtNetwork import QNetworkRequest

from ....Settings import Settings
from ...PreferencesHelper import PreferencesHelper
from ...api.AbstractApiClient import AbstractApiClient
from ...api.JsonObject import JsonObject


class MyMiniFactoryApiClient(AbstractApiClient):
    """ Client for interacting with the MyMiniFactory API. """
    
    def __init__(self) -> None:
        super().__init__()
        PreferencesHelper.initSetting(Settings.MYMINIFACTORY_USER_NAME_PREFERENCES_KEY, "")

    @property
    def available_views(self) -> List[str]:
        return ["My Likes", "My Collections", "My Things", "Popular", "Featured", "Newest"]

    @property
    def user_id(self) -> str:
        return PreferencesHelper.getSettingValue(Settings.MYMINIFACTORY_USER_NAME_PREFERENCES_KEY)

    def getThingsFromCollectionQuery(self, collection_id: int) -> str:
        return "collections/{}".format(collection_id)
    
    def getThingsLikedByUserQuery(self) -> str:
        return "users/{}/objects_liked".format(self.user_id)
    
    def getThingsByUserQuery(self) -> str:
        return "users/{}/objects".format(self.user_id)
    
    def getThingsMadeByUserQuery(self) -> str:
        raise NotImplementedError("Provider 'MyMiniFactory' does not support user-made things.")
    
    def getPopularThingsQuery(self) -> str:
        return "search?sort=popularity"

    def getFeaturedThingsQuery(self) -> str:
        return "search?featured=1"

    def getNewestThingsQuery(self) -> str:
        return "search?sort=date"
    
    def getThingsBySearchQuery(self, search_terms: str) -> str:
        return ""

    def getThing(self, thing_id: int, on_finished: Callable[[JsonObject], Any],
                 on_failed: Optional[Callable[[JsonObject], Any]] = None) -> None:
        url = "{}/objects/{}".format(self._root_url, thing_id)
        reply = self._manager.get(self._createEmptyRequest(url))
        self._addCallback(reply, on_finished, on_failed)
        
    def getCollections(self, on_finished: Callable[[List[JsonObject]], Any],
                       on_failed: Optional[Callable[[JsonObject], Any]]) -> None:
        pass  # TODO

    def getThingFiles(self, thing_id: int, on_finished: Callable[[List[JsonObject]], Any],
                      on_failed: Optional[Callable[[JsonObject], Any]] = None) -> None:
        url = "{}/objects/{}".format(self._root_url, thing_id)
        reply = self._manager.get(self._createEmptyRequest(url))
        self._addCallback(reply, on_finished, on_failed)

    def downloadThingFile(self, file_id: int, file_name: str, on_finished: Callable[[bytes], Any]) -> None:
        url = "https://www.myminifactory.com/download/{}?downloadfile={}".format(file_id, file_name)
        reply = self._manager.get(self._createEmptyRequest(url))
        self._addCallback(reply, on_finished)

    def getThings(self, query: str, page: int, on_finished: Callable[[List[JsonObject]], Any],
                  on_failed: Optional[Callable[[JsonObject], Any]] = None) -> None:
        url = "{}/{}&per_page={}&page={}".format(self._root_url, query, Settings.PER_PAGE, page)
        reply = self._manager.get(self._createEmptyRequest(url))
        self._addCallback(reply, on_finished, on_failed)

    @property
    def _root_url(self):
        return "https://www.myminifactory.com/api/v2"

    def _setAuth(self, request: QNetworkRequest):
        pass  # TODO
