# Copyright (c) 2020.
# Thingiverse plugin is released under the terms of the LGPLv3 or higher.
from typing import List, Callable, Any, Optional, Tuple

from PyQt5.QtNetwork import QNetworkRequest, QNetworkReply

from ...Settings import Settings
from ...PreferencesHelper import PreferencesHelper
from ...api.AbstractApiClient import AbstractApiClient
from ...api.ApiHelper import ApiHelper
from ...api.JsonObject import ApiError, Thing, ThingFile, Collection
from ...api.LocalAuthService import LocalAuthService


class ThingiverseApiClient(AbstractApiClient):
    """ Client for interacting with the Thingiverse API. """

    def __init__(self) -> None:
        self._auth_state = None  # type: Optional[str]
        PreferencesHelper.initSetting(Settings.THINGIVERSE_USER_NAME_PREFERENCES_KEY)
        PreferencesHelper.initSetting(Settings.THINGIVERSE_API_TOKEN_KEY)
        super().__init__()

    @property
    def user_id(self):
        user_name = PreferencesHelper.getSettingValue(Settings.THINGIVERSE_USER_NAME_PREFERENCES_KEY)
        if not user_name or user_name == "":
            return "404_this_user_does_not_exist"  # ugly, but tricks the Thingiverse API in giving a 404 response
        return user_name

    def authenticate(self) -> None:
        pass
        # FIXME: Waiting for Thingiverse app approval
        # self._auth_state = "thingiverse_{}".format(str(time.time()))
        # url = "{}?{}".format("https://www.thingiverse.com/login/oauth/authorize", urlencode({
        #     "client_id": Settings.THINGIVERSE_CLIENT_ID,
        #     "response_type": "token",
        #     "state": self._auth_state
        # }))
        # LocalAuthService.onTokenReceived.connect(self._onTokenReceived)
        # LocalAuthService.start(url)

    def clearAuthentication(self) -> None:
        PreferencesHelper.setSetting(Settings.THINGIVERSE_API_TOKEN_KEY, "")

    def _onTokenReceived(self, state: str, token: Optional[str] = None) -> None:
        if state != self._auth_state:
            return
        LocalAuthService.onTokenReceived.disconnect(self._onTokenReceived)
        if not token:
            return
        PreferencesHelper.setSetting(Settings.THINGIVERSE_API_TOKEN_KEY, token)

    def getThingsFromCollectionQuery(self, collection_id: str) -> str:
        return "collections/{}/things".format(collection_id)

    def getThingsBySearchQuery(self, search_terms: str) -> str:
        return "search/{}".format(search_terms)

    def getThingsLikedByUserQuery(self) -> str:
        return "users/{}/likes".format(self.user_id)

    def getThingsByUserQuery(self) -> str:
        return "users/{}/things".format(self.user_id)

    def getThingsMadeByUserQuery(self) -> str:
        return "users/{}/copies".format(self.user_id)

    def getPopularThingsQuery(self) -> str:
        return "popular"

    def getFeaturedThingsQuery(self) -> str:
        return "featured"

    def getNewestThingsQuery(self) -> str:
        return "newest"

    def getCollections(self, on_finished: Callable[[List[Collection]], Any],
                       on_failed: Optional[Callable[[Optional[ApiError], Optional[int]], Any]] = None) -> None:
        url = "{}/users/{}/collections".format(self._root_url, self.user_id)
        reply = self._manager.get(self._createEmptyRequest(url))
        self._addCallback(reply, on_finished, on_failed, parser=self._parseGetCollections)

    @staticmethod
    def _parseGetCollections(reply: QNetworkReply) -> Tuple[int, Optional[List[Collection]]]:
        status_code, response = ApiHelper.parseReplyAsJson(reply)
        if status_code == 404:
            # Thingiverse returns a 404 when there are no collection results instead of just an empty list
            return 200, []
        if not response or not isinstance(response, list):
            return status_code, None
        return status_code, [Collection({
            "id": item.get("id"),
            "thumbnail": item.get("thumbnail"),
            "name": item.get("name"),
            "description": item.get("description"),
            "url": item.get("creator", {}).get("public_url")
        }) for item in response]

    def getThings(self, query: str, page: int, on_finished: Callable[[List[Thing]], Any],
                  on_failed: Optional[Callable[[Optional[ApiError], Optional[int]], Any]] = None) -> None:
        url = "{}/{}?per_page={}&page={}".format(self._root_url, query, Settings.PER_PAGE, page)
        reply = self._manager.get(self._createEmptyRequest(url))
        self._addCallback(reply, on_finished, on_failed, parser=self._parseGetThings)

    @staticmethod
    def _parseGetThings(reply: QNetworkReply) -> Tuple[int, Optional[List[Thing]]]:
        status_code, response = ApiHelper.parseReplyAsJson(reply)
        if status_code == 404:
            # Thingiverse returns a 404 when there are no thing results instead of just an empty list
            return 200, []
        if isinstance(response, dict) and "hits" in response:
            # Thingiverse decided to change their API response for /search and put the actual results in a 'hits' field
            response = response["hits"]
        if not response or not isinstance(response, list):
            # Thingiverse returns 'None' in the 'hits' field when there are no results instead of an empty list
            return status_code, []
        return status_code, [Thing({
            "id": item.get("id"),
            "thumbnail": item.get("thumbnail"),
            "name": item.get("thing", {}).get("name") if item.get("thing") else item.get("name"),
            "url": item.get("public_url") or item.get("url"),
            "description": item.get("description_html") or item.get("description")
        }) for item in response]

    def getThing(self, thing_id: int, on_finished: Callable[[Thing], Any],
                 on_failed: Optional[Callable[[Optional[ApiError], Optional[int]], Any]] = None) -> None:
        url = "{}/things/{}".format(self._root_url, thing_id)
        reply = self._manager.get(self._createEmptyRequest(url))
        self._addCallback(reply, on_finished, on_failed, parser=self._parseGetThing)

    @staticmethod
    def _parseGetThing(reply: QNetworkReply) -> Tuple[int, Optional[Thing]]:
        status_code, item = ApiHelper.parseReplyAsJson(reply)
        if not item or not isinstance(item, dict):
            return status_code, None
        return status_code, Thing({
            "id": item.get("id"),
            "thumbnail": item.get("thumbnail"),
            "name": item.get("name"),
            "url": item.get("public_url") or item.get("url"),
            "description": item.get("description_html") or item.get("description")
        })

    def getThingFiles(self, thing_id: int, on_finished: Callable[[List[ThingFile]], Any],
                      on_failed: Optional[Callable[[Optional[ApiError], Optional[int]], Any]] = None) -> None:
        url = "{}/things/{}/files".format(self._root_url, thing_id)
        reply = self._manager.get(self._createEmptyRequest(url))
        self._addCallback(reply, on_finished, on_failed, parser=self._parseGetThingFiles)

    @staticmethod
    def _parseGetThingFiles(reply: QNetworkReply) -> Tuple[int, Optional[List[ThingFile]]]:
        status_code, response = ApiHelper.parseReplyAsJson(reply)
        if not response or not isinstance(response, list):
            return status_code, None
        return status_code, [ThingFile({
            "id": item.get("id"),
            "thumbnail": item.get("thumbnail"),
            "name": item.get("name"),
            "url": item.get("public_url") or item.get("url"),
        }) for item in response]

    def downloadThingFile(self, file_id: int, file_name: str, on_finished: Callable[[bytes], Any]) -> None:
        url = "{}/files/{}/download".format(self._root_url, file_id)
        reply = self._manager.get(self._createEmptyRequest(url))
        self._addCallback(reply, on_finished, parser=ApiHelper.parseReplyAsBytes)

    @property
    def _root_url(self):
        return "https://api.thingiverse.com"

    def _setAuth(self, request: QNetworkRequest) -> None:
        # FIXME: Waiting for Thingiverse app approval
        # token = PreferencesHelper.getSettingValue(Settings.THINGIVERSE_API_TOKEN_KEY)
        # if not token or token == "":
        #     # If the user was not signed in we use a default token for the public endpoints.
        #     token = Settings.THINGIVERSE_API_TOKEN
        request.setRawHeader(b"Authorization", "Bearer {}".format(Settings.THINGIVERSE_API_TOKEN).encode())
