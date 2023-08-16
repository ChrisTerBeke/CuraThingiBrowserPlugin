# Copyright (c) 2020.
# Thingiverse plugin is released under the terms of the LGPLv3 or higher.
import time
from typing import List, Callable, Any, Optional, Tuple
from urllib.parse import urlencode

from PyQt6.QtCore import QUrl
from PyQt6.QtNetwork import QNetworkRequest, QNetworkReply

from ...Settings import Settings
from ...PreferencesHelper import PreferencesHelper
from ...api.ApiHelper import ApiHelper
from ...api.AbstractApiClient import AbstractApiClient
from ...api.JsonObject import ApiError, Collection, Thing, ThingFile, UserData
from ...api.LocalAuthService import LocalAuthService


class MyMiniFactoryApiClient(AbstractApiClient):
    """ Client for interacting with the MyMiniFactory API. """

    def __init__(self) -> None:
        self._username: Optional[str] = None
        self._auth_state: Optional[str] = None
        access_token = PreferencesHelper.initSetting(Settings.MYMINIFACTORY_API_TOKEN_KEY)
        if access_token and access_token != "":
            self._getUserData()
        super().__init__()

    def authenticate(self) -> None:
        self._auth_state = "myminifactory_{}".format(str(time.time()))
        url = "{}?{}".format("https://auth.myminifactory.com/web/authorize", urlencode({
            "client_id": Settings.MYMINIFACTORY_CLIENT_ID,
            "redirect_uri": "http://localhost:55444/callback",
            "response_type": "token",
            "state": self._auth_state
        }))
        LocalAuthService.onTokenReceived.connect(self._onTokenReceived)
        LocalAuthService.start(url)

    def clearAuthentication(self) -> None:
        PreferencesHelper.setSetting(Settings.MYMINIFACTORY_API_TOKEN_KEY, "")

    def _onTokenReceived(self, state: str, token: Optional[str] = None) -> None:
        if state != self._auth_state:
            return
        LocalAuthService.onTokenReceived.disconnect(self._onTokenReceived)
        if not token:
            return
        PreferencesHelper.setSetting(Settings.MYMINIFACTORY_API_TOKEN_KEY, token)
        self._getUserData()

    def _getUserData(self) -> None:
        url = "{}/user".format(self._root_url)
        reply = self._manager.get(self._createEmptyRequest(url)) or self._createEmptyReply()
        self._addCallback(reply, on_finished=self._onGetUserData, parser=self._parseGetUserData)
        # FIXME: handle error response

    @staticmethod
    def _parseGetUserData(reply: QNetworkReply) -> Tuple[int, Optional[UserData]]:
        status_code, data = ApiHelper.parseReplyAsJson(reply)
        if not data or not isinstance(data, dict):
            return status_code, None
        return status_code, UserData({"username": data.get("username", "")})

    def _onGetUserData(self, user: UserData) -> None:
        self._username = user.username

    def getThingsFromCollectionQuery(self, collection_id: str) -> str:
        return "collections/{}".format(collection_id)

    def getThingsLikedByUserQuery(self) -> str:
        return "users/{}/objects_liked".format(self._username)

    def getThingsByUserQuery(self) -> str:
        return "users/{}/objects".format(self._username)

    def getThingsMadeByUserQuery(self) -> str:
        return "users/{}/objects".format(self._username)

    def getPopularThingsQuery(self) -> str:
        return "search?sort=popularity"

    def getFeaturedThingsQuery(self) -> str:
        return "search?featured=1"

    def getNewestThingsQuery(self) -> str:
        return "search?sort=date"

    def getThingsBySearchQuery(self, search_terms: str) -> str:
        return "search?q={}".format(search_terms)

    def getThing(self, thing_id: int, on_finished: Callable[[Thing], Any],
                 on_failed: Optional[Callable[[Optional[ApiError], Optional[int]], Any]] = None) -> None:
        url = "{}/objects/{}".format(self._root_url, thing_id)
        reply = self._manager.get(self._createEmptyRequest(url)) or self._createEmptyReply()
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
                       on_failed: Optional[Callable[[Optional[ApiError], Optional[int]], Any]]) -> None:
        url = "{}/users/{}/collections".format(self._root_url, self._username)
        reply = self._manager.get(self._createEmptyRequest(url)) or self._createEmptyReply()
        self._addCallback(reply, on_finished, on_failed, parser=self._parseGetCollections)

    @staticmethod
    def _parseGetCollections(reply: QNetworkReply) -> Tuple[int, Optional[List[Collection]]]:
        status_code, response = ApiHelper.parseReplyAsJson(reply)
        if not response or not isinstance(response, dict):
            return status_code, None
        items = response.get("items", [])
        return status_code, [Collection({
            "id": item.get("id"),
            "thumbnail": item.get("cover_object", {}).get("images", [])[0].get("thumbnail", {}).get("url")
            if item.get("cover_object") else None,
            "name": item.get("name"),
            "url": item.get("url"),
            "description": item.get("description")
        }) for item in items]

    def getThings(self, query: str, page: int, on_finished: Callable[[List[Thing]], Any],
                  on_failed: Optional[Callable[[Optional[ApiError], Optional[int]], Any]] = None) -> None:
        operator = "&" if query.find("?") > 0 else "?"
        url = "{}/{}{}per_page={}&page={}".format(self._root_url, query, operator, Settings.PER_PAGE, page)
        reply = self._manager.get(self._createEmptyRequest(url)) or self._createEmptyReply()
        self._addCallback(reply, on_finished, on_failed, parser=self._parseGetThings)

    @staticmethod
    def _parseGetThings(reply: QNetworkReply) -> Tuple[int, Optional[List[Thing]]]:
        status_code, response = ApiHelper.parseReplyAsJson(reply)
        if not response or not isinstance(response, dict):
            return status_code, None
        items = response.get("objects", {}).get("items", []) if response.get("objects", {}) else response.get("items", [])
        return status_code, [Thing({
            "id": item.get("id"),
            "thumbnail": item.get("images", [])[0].get("thumbnail", {}).get("url") if item.get("images") else None,
            "name": item.get("name"),
            "url": item.get("url"),
            "description": item.get("description"),
        }) for item in items]

    def getThingFiles(self, thing_id: int, on_finished: Callable[[List[ThingFile]], Any],
                      on_failed: Optional[Callable[[Optional[ApiError], Optional[int]], Any]] = None) -> None:
        url = "{}/objects/{}".format(self._root_url, thing_id)
        reply = self._manager.get(self._createEmptyRequest(url)) or self._createEmptyReply()
        self._addCallback(reply, on_finished, on_failed, parser=self._parseGetThingFiles)

    @staticmethod
    def _parseGetThingFiles(reply: QNetworkReply) -> Tuple[int, Optional[List[ThingFile]]]:
        status_code, response = ApiHelper.parseReplyAsJson(reply)
        if not response or not isinstance(response, dict):
            return status_code, None
        items = response.get("files", {}).get("items")
        return status_code, [ThingFile({
            "id": item.get("id"),
            "name": item.get("filename"),
            "thumbnail": item.get("thumbnail_url"),
            "download_url": item.get("download_url"),
        }) for item in items]

    @property
    def _root_url(self):
        return "https://www.myminifactory.com/api/v2"

    def _setAuth(self, request: QNetworkRequest) -> QNetworkRequest:
        token = PreferencesHelper.getSettingValue(Settings.MYMINIFACTORY_API_TOKEN_KEY)
        if not token or token == "":
            current_url = request.url().toString()
            operator = "&" if current_url.find("?") > 0 else "?"
            new_url = QUrl("{}{}key={}".format(current_url, operator, Settings.MYMINIFACTORY_API_TOKEN))
            request.setUrl(new_url)
        else:
            request.setRawHeader(self._strToByteArray("Authorization"), self._strToByteArray("Bearer {}".format(token)))
        return request
