# Copyright (c) 2020 Chris ter Beke.
# Thingiverse plugin is released under the terms of the LGPLv3 or higher.
from typing import List, Callable, Any, Optional, Tuple

from PyQt5.QtCore import QUrl
from PyQt5.QtNetwork import QNetworkRequest, QNetworkReply

from ...Settings import Settings
from ...PreferencesHelper import PreferencesHelper
from ...api.ApiHelper import ApiHelper
from ...api.AbstractApiClient import AbstractApiClient
from ...api.JsonObject import ApiError, Collection, Thing, ThingFile


class MyMiniFactoryApiClient(AbstractApiClient):
    """ Client for interacting with the MyMiniFactory API. """

    def __init__(self) -> None:
        super().__init__()
        PreferencesHelper.initSetting(Settings.MYMINIFACTORY_USER_NAME_PREFERENCES_KEY, "")

    @property
    def available_views(self) -> List[str]:
        return ["userLikes", "userCollections", "userThings", "popular", "featured", "newest"]

    @property
    def user_id(self) -> str:
        return PreferencesHelper.getSettingValue(Settings.MYMINIFACTORY_USER_NAME_PREFERENCES_KEY)

    def getThingsFromCollectionQuery(self, collection_id: str) -> str:
        return "collections/{}".format(collection_id)

    def getThingsLikedByUserQuery(self) -> str:
        return "users/{}/objects_liked".format(self.user_id)

    def getThingsByUserQuery(self) -> str:
        return "users/{}/objects".format(self.user_id)

    def getThingsMadeByUserQuery(self) -> str:
        return "users/{}/objects".format(self.user_id)

    def getPopularThingsQuery(self) -> str:
        return "search?sort=popularity"

    def getFeaturedThingsQuery(self) -> str:
        return "search?featured=1"

    def getNewestThingsQuery(self) -> str:
        return "search?sort=date"

    def getThingsBySearchQuery(self, search_terms: str) -> str:
        return "search?q={}".format(search_terms)

    def getThing(self, thing_id: int, on_finished: Callable[[Thing], Any],
                 on_failed: Optional[Callable[[Optional[ApiError]], Any]] = None) -> None:
        url = "{}/objects/{}".format(self._root_url, thing_id)
        reply = self._manager.get(self._createEmptyRequest(url))
        self._addCallback(reply, on_finished, on_failed, parser=self._parseGetThing)

    @staticmethod
    def _parseGetThing(reply: QNetworkReply) -> Tuple[int, Optional[Thing]]:
        status_code, item = ApiHelper.parseReplyAsJson(reply)
        if not item or not isinstance(item, dict):
            return status_code, None
        return status_code, Thing({
            "id": item.get("id"),
            "thumbnail": item.get("images", [])[0].get("thumbnail", {}).get("url") if item.get("images") else None,
            "name": item.get("name"),
            "url": item.get("url"),
            "description": item.get("description")
        })

    def getCollections(self, on_finished: Callable[[List[Collection]], Any],
                       on_failed: Optional[Callable[[Optional[ApiError]], Any]]) -> None:
        url = "{}/users/{}/collections".format(self._root_url, self.user_id)
        reply = self._manager.get(self._createEmptyRequest(url))
        self._addCallback(reply, on_finished, on_failed, parser=self._parseGetCollections)

    @staticmethod
    def _parseGetCollections(reply: QNetworkReply) -> Tuple[int, Optional[List[Collection]]]:
        status_code, response = ApiHelper.parseReplyAsJson(reply)
        if not response or not isinstance(response, dict):
            return status_code, None
        return status_code, [Collection({
            "id": item.get("id"),
            "thumbnail": item.get("cover_object", {}).get("images", []).get(0).get("thumbnail", {}).get("url")
            if item.get("cover_object") else None,
            "name": item.get("name"),
            "url": item.get("url"),
            "description": item.get("description")
        }) for item in response.get("items", [])]

    def getThingFiles(self, thing_id: int, on_finished: Callable[[List[ThingFile]], Any],
                      on_failed: Optional[Callable[[Optional[ApiError]], Any]] = None) -> None:
        url = "{}/objects/{}".format(self._root_url, thing_id)
        reply = self._manager.get(self._createEmptyRequest(url))
        self._addCallback(reply, on_finished, on_failed, parser=self._parseGetThingFiles)

    @staticmethod
    def _parseGetThingFiles(reply: QNetworkReply) -> Tuple[int, Optional[List[ThingFile]]]:
        status_code, response = ApiHelper.parseReplyAsJson(reply)
        if not response or not isinstance(response, dict):
            return status_code, None
        file_id = response.get("id")
        items = response.get("files", {}).get("items")
        return status_code, [ThingFile({
            "id": file_id,
            "thumbnail": item.get("thumbnail_url"),
            "name": item.get("filename"),
            "url": None,
        }) for item in items]

    def getThings(self, query: str, page: int, on_finished: Callable[[List[Thing]], Any],
                  on_failed: Optional[Callable[[Optional[ApiError]], Any]] = None) -> None:
        operator = "&" if query.find("?") > 0 else "?"
        url = "{}/{}{}per_page={}&page={}".format(self._root_url, query, operator, Settings.PER_PAGE, page)
        reply = self._manager.get(self._createEmptyRequest(url))
        self._addCallback(reply, on_finished, on_failed, parser=self._parseGetThings)

    @staticmethod
    def _parseGetThings(reply: QNetworkReply) -> Tuple[int, Optional[List[Thing]]]:
        status_code, response = ApiHelper.parseReplyAsJson(reply)
        if not response or not isinstance(response, dict):
            return status_code, None
        items = response.get("objects", {}).get("items") if response.get("objects") else response.get("items")
        return status_code, [Thing({
            "id": item.get("id"),
            "thumbnail": item.get("images", [])[0].get("thumbnail", {}).get("url") if item.get("images") else None,
            "name": item.get("name"),
            "url": item.get("url"),
            "description": item.get("description")
        }) for item in items]

    def downloadThingFile(self, file_id: int, file_name: str, on_finished: Callable[[bytes], Any]) -> None:
        url = "https://www.myminifactory.com/download/{}?downloadfile={}".format(file_id, file_name)
        reply = self._manager.get(self._createEmptyRequest(url))
        self._addCallback(reply, on_finished, parser=ApiHelper.parseReplyAsBytes)

    @property
    def _root_url(self):
        return "https://www.myminifactory.com/api/v2"

    def _setAuth(self, request: QNetworkRequest):
        current_url = request.url().toString()
        operator = "&" if current_url.find("?") > 0 else "?"
        new_url = QUrl("{}{}key={}".format(current_url, operator, Settings.MYMINIFACTORY_API_TOKEN))
        request.setUrl(new_url)
