# Copyright (c) 2018 Chris ter Beke.
# Thingiverse plugin is released under the terms of the LGPLv3 or higher.
from typing import List, Callable, Any, Union, Dict, Tuple, Optional, cast

from PyQt5.QtCore import QUrl, QObject
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkReply, QNetworkRequest

from UM.Logger import Logger
from cura.CuraApplication import CuraApplication

from ..Settings import Settings  # type: ignore
from ..api.APIClient import ApiClient  # type: ignore
from ..api.JSONObject import JSONObject, Collection, Thing, ThingFile  # type: ignore

class MyMiniFactoryApiClient(ApiClient):
    """ Client for interacting with the MyMiniFactory API. """

    # API constants.
    @property
    def _root_url(self):
        return "https://www.myminifactory.com/api/v2"

    @property
    def _auth(self):
        return "Query Key", "key={}".format(Settings.MYMINIFACTORY_API_TOKEN)

    @property
    def user_id(self):
        return CuraApplication.getInstance().getPreferences().getValue(Settings.MYMINIFACTORY_USER_NAME_PREFERENCES_KEY)

    def getSearchUrl(self, term: str) -> str:
        return "search?q={}".format(term)

    def getUserCollections(self, on_finished: Callable[[JSONObject], Any],
                                 on_failed: Optional[Callable[[JSONObject], Any]]) -> None:
        url = "{}/users/{}/collections".format(self._root_url, self.user_id)
        reply = self._manager.get(self._createEmptyRequest(url))

        def convertResponse(response) -> None:
            _collections = [MyMiniFactoryApiClient._jsonCollectionDecoder(collection) for collection in response.items] if response.items else []
            on_finished(_collections)

        self._anti_gc_callbacks.append(convertResponse)
        self._addCallback(reply, convertResponse, on_failed)

    def getCollection(self, collection_id: int, on_finished: Callable[[JSONObject], Any],
                                                on_failed: Optional[Callable[[JSONObject], Any]]) -> None:
        url = "collections/{}".format(collection_id)
        
        def convert_response(response) -> None:
            _things = [MyMiniFactoryApiClient._jsonThingDecoder(thing) for thing in response.objects.items] if response.objects and response.objects.items else []
            on_finished(_things)

        self.get(url, 1, on_finished, on_failed, convert_response)

    def getLikesUrl(self) -> str:
        url = "users/{}/objects_liked".format(self.user_id)
        return url

    def getUserThingsUrl(self) -> str:
        return "users/{}/objects".format(self.user_id)

    def getUserMakesUrl(self) -> str:
        pass

    def getPopularUrl(self) -> str:
        return "search?sort=popularity"

    def getFeaturedUrl(self) -> str:
        return "search?featured=1"

    def getNewestUrl(self) -> str:
        return "search?sort=date"

    def getThing(self, thing_id: int, on_finished: Callable[[JSONObject], Any],
                 on_failed: Optional[Callable[[JSONObject], Any]] = None) -> None:
        """
        Get a single thing by ID.
        :param thing_id: The thing ID.
        :param on_finished: Callback method to receive the async result on.
        :param on_failed: Callback method to receive failed request on.
        """
        url = "{}/objects/{}".format(self._root_url, thing_id)
        reply = self._manager.get(self._createEmptyRequest(url))

        def convertResponse(response) -> None:
            on_finished(MyMiniFactoryApiClient._jsonThingDecoder(response) if response else None)

        self._anti_gc_callbacks.append(convertResponse)
        self._addCallback(reply, convertResponse, on_failed)

    def getThingFiles(self, thing_id: int, on_finished: Callable[[List[JSONObject]], Any],
                      on_failed: Optional[Callable[[JSONObject], Any]] = None) -> None:
        """
        Get a thing's files by ID.
        :param thing_id: The thing ID.
        :param on_finished: Callback method to receive the async result on.
        :param on_failed: Callback method to receive failed request on.
        """
        url = "{}/objects/{}".format(self._root_url, thing_id)
        reply = self._manager.get(self._createEmptyRequest(url))

        def convertResponse(response) -> None:
            _files = [MyMiniFactoryApiClient._jsonThingFileDecoder(file_data, response.id) for file_data in response.files.items] if response.files and response.files.items else []
            on_finished(_files)

        self._anti_gc_callbacks.append(convertResponse)
        self._addCallback(reply, convertResponse, on_failed)

    def downloadThingFile(self, file_id: int, file_name: str, on_finished: Callable[[bytes], Any]) -> None:
        """
        Download a thing file by its ID.
        :param file_id: The file ID to download.
        :param on_finished: Callback method to receive the async result on as bytes.
        """
        # Have to remove the /api/v2 portion of the root for this particual endpoint
        url = "{}/download/{}?downloadfile={}".format(self._root_url[: -7], file_id, file_name)
        Logger.log('i', "Download URL: {}".format(url))
        reply = self._manager.get(self._createEmptyRequest(url))

        # We use a custom parse function for this API call because the response is not a JSON model.
        def parse() -> None:
            result = bytes(reply.readAll())
            self._anti_gc_callbacks.remove(parse)
            on_finished_cast = cast(Callable[[bytes], Any], on_finished)
            on_finished_cast(result)

        self._anti_gc_callbacks.append(parse)
        reply.finished.connect(parse)

    def get(self, query: str, page: int, on_finished: Callable[[List[JSONObject]], Any],
            on_failed: Optional[Callable[[JSONObject], Any]] = None,
            convert_response: Optional[Callable[[JSONObject], Any]] = None) -> None:
        """
        Get things by query.
        :param query: The things to get.
        :param page: Page number of query results (for pagination).
        :param on_finished: Callback method to receive the async result on.
        :param on_failed: Callback method to receive failed request on.
        """
        operator = "?"
        if query.find("?") > -1:
            operator = "&"
        url = "{}/{}{}per_page={}&page={}".format(self._root_url, query, operator, Settings.MYMINIFACTORY_API_PER_PAGE, page)
        Logger.log('i', 'GET URL: {}'.format(url))
        reply = self._manager.get(self._createEmptyRequest(url))

        if not convert_response:
            def convert_response(response) -> None:
                _things = [MyMiniFactoryApiClient._jsonThingDecoder(thing) for thing in response.items] if response.items else []
                on_finished(_things)

        self._anti_gc_callbacks.append(convert_response)
        self._addCallback(reply, convert_response, on_failed, request_url=url)

    @staticmethod
    def _jsonCollectionDecoder(data: JSONObject) -> Collection:
        return Collection({
            'URL': data.url,
            'ID': data.id,
            'NAME': data.name,
            'DESCRIPTION': data.description if hasattr(data, 'description') else None,
            'THUMBNAIL': data.cover_object.images[0].thumbnail.url if hasattr(data, 'cover_object') else None
        })

    @staticmethod
    def _jsonThingDecoder(data: JSONObject) -> Thing:
        return Thing({
            'URL': data.url,
            'ID': data.id,
            'NAME': data.name,
            'DESCRIPTION': data.description if hasattr(data, 'description') else None,
            'THUMBNAIL': data.images[0].thumbnail.url if hasattr(data, 'images') else None
        })

    @staticmethod
    def _jsonThingFileDecoder(data: JSONObject, thing_id: int) -> ThingFile:
        return ThingFile({
            'URL': None,
            'ID': thing_id, # MyMiniFactory needs the thing's id instead of file id
            'NAME': data.filename,
            'THUMBNAIL': data.thumbnail_url
        })
