# Copyright (c) 2018 Chris ter Beke.
# Thingiverse plugin is released under the terms of the LGPLv3 or higher.
from typing import List, Callable, Any, Union, Optional, cast

from cura.CuraApplication import CuraApplication

from ..Settings import Settings  # type: ignore
from ..api.APIClient import ApiClient  # type: ignore
from ..api.JSONObject import JSONObject, Collection, Thing, ThingFile  # type: ignore

from UM.Logger import Logger

class ThingiverseApiClient(ApiClient):
    """ Client for interacting with the Thingiverse API. """

    # API constants.
    @property
    def _root_url(self):
        return "https://api.thingiverse.com"

    @property
    def _auth(self):
        return "Authorization", "Bearer {}".format(Settings.THINGIVERSE_API_TOKEN).encode()

    @property
    def user_id(self):
        return CuraApplication.getInstance().getPreferences().getValue(Settings.THINGIVERSE_USER_NAME_PREFERENCES_KEY)

    def getSearchUrl(self, term: str) -> str:
        """
        Get URL path for seraching for an object
        :param term: Term to use in search
        :return: Formatted URL path
        """
        return "search/{}/?sort=relevent".format(term)

    def getUserCollections(self, on_finished: Callable[[JSONObject], Any],
                                 on_failed: Optional[Callable[[JSONObject], Any]]) -> None:
        """
        Get user's collections
        :param on_finished: Callback with user's collections
        :param on_failed: Callback with server response
        """
        url = "{}/users/{}/collections".format(self._root_url, self.user_id)
        reply = self._manager.get(self._createEmptyRequest(url))

        def convert_response(response) -> None:
            _collections = [ThingiverseApiClient._jsonCollectionDecoder(collection) for collection in response] if response else []
            on_finished(_collections)

        self._anti_gc_callbacks.append(convert_response)
        self._addCallback(reply, convert_response, on_failed)

    def getCollection(self, collection_id: int, on_finished: Callable[[JSONObject], Any],
                                                on_failed: Optional[Callable[[JSONObject], Any]]) -> None:
        """
        Get a specific collection's objects
        :param collection_id: ID of the collection
        :param on_finished: Callback with user's collections
        :param on_failed: Callback with server response
        """
        url = "collections/{}/things".format(collection_id)
        self.get(url, 1, on_finished, on_failed)

    def getLikesUrl(self) -> str:
        """
        Get URL path for a user's liked objects
        :return: Formatted URL path
        """
        return "users/{}/likes".format(self.user_id)

    def getUserThingsUrl(self) -> str:
        """
        Get URL path for a user's uploaded objects
        :return: Formatted URL path
        """
        return "users/{}/things".format(self.user_id)

    def getUserMakesUrl(self) -> str:
        """
        Get URL path for a user's printed objects
        :return: Formatted URL path
        """
        return "users/{}/copies".format(self.user_id)

    def getPopularUrl(self) -> str:
        """
        Get URL path for most popular objects
        :return: Formatted URL path
        """
        return "popular"

    def getFeaturedUrl(self) -> str:
        """
        Get URL path for featured objects
        :return: Formatted URL path
        """
        return "featured"

    def getNewestUrl(self) -> str:
        """
        Get URL path for the newest objects
        :return: Formatted URL path
        """
        return "newest"

    def getThing(self, thing_id: int, on_finished: Callable[[JSONObject], Any],
                 on_failed: Optional[Callable[[JSONObject], Any]] = None) -> None:
        """
        Get a single thing by ID.
        :param thing_id: The thing ID.
        :param on_finished: Callback method to receive the async result on.
        :param on_failed: Callback method to receive failed request on.
        """
        url = "{}/things/{}".format(self._root_url, thing_id)
        reply = self._manager.get(self._createEmptyRequest(url))

        def convert_response(response) -> None:
            on_finished(ThingiverseApiClient._jsonThingDecoder(response) if response else None)

        self._anti_gc_callbacks.append(convert_response)
        self._addCallback(reply, convert_response, on_failed)

    def getThingFiles(self, thing_id: int, on_finished: Callable[[List[JSONObject]], Any],
                      on_failed: Optional[Callable[[JSONObject], Any]] = None) -> None:
        """
        Get a thing's files by ID.
        :param thing_id: The thing ID.
        :param on_finished: Callback method to receive the async result on.
        :param on_failed: Callback method to receive failed request on.
        """
        url = "{}/things/{}/files".format(self._root_url, thing_id)
        reply = self._manager.get(self._createEmptyRequest(url))

        def convert_response(response) -> None:
            _files = [ThingiverseApiClient._jsonThingFileDecoder(thing) for thing in response] if response else []
            on_finished(_files)

        self._anti_gc_callbacks.append(convert_response)
        self._addCallback(reply, convert_response, on_failed)

    def downloadThingFile(self, file_id: int, file_name: str, on_finished: Callable[[bytes], Any]) -> None:
        """
        Download a thing file by its ID.
        :param file_id: The file ID to download.
        :param file_name: The file's name including extension
        :param on_finished: Callback method to receive the async result on as bytes.
        """
        url = "{}/files/{}/download".format(self._root_url, file_id)
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
        :param convert_response: Callback to convert the response
        """
        operator = "?"
        if query.find("?") > -1:
            operator = "&"
        url = "{}/{}{}per_page={}&page={}".format(self._root_url, query, operator, Settings.THINGIVERSE_API_PER_PAGE, page)
        reply = self._manager.get(self._createEmptyRequest(url))

        if not convert_response:
            def convert_response(response) -> None:
                _things = [ThingiverseApiClient._jsonThingDecoder(thing) for thing in response] if response else []
                on_finished(_things)

        self._anti_gc_callbacks.append(convert_response)
        self._addCallback(reply, convert_response, on_failed)

    @staticmethod
    def _jsonCollectionDecoder(data: JSONObject) -> Collection:
        """
        Function to convert JSONObject into a Collection object
        :param data: JSONObject with key-value translated values
        """
        return Collection({
            'URL': data.url,
            'ID': data.id,
            'NAME': data.name,
            'DESCRIPTION': data.description if hasattr(data, 'description') else None,
            'THUMBNAIL': data.thumbnail if hasattr(data, 'thumbnail') else None
        })

    @staticmethod
    def _jsonThingDecoder(data: JSONObject) -> Thing:
        """
        Function to convert JSONObject into a Thing object
        :param data: JSONObject with key-value translated values
        """
        return Thing({
            'URL': data.public_url,
            'ID': data.id,
            'NAME': data.name,
            'DESCRIPTION': data.description if hasattr(data, 'description') else None,
            'THUMBNAIL': data.thumbnail if hasattr(data, 'thumbnail') else None
        })

    @staticmethod
    def _jsonThingFileDecoder(data: JSONObject) -> ThingFile:
        """
        Function to convert JSONObject into a ThingFile object
        :param data: JSONObject with key-value translated values
        """
        return ThingFile({
            'URL': data.public_url if hasattr(data, 'public_url') else data.url,
            'ID': data.id,
            'NAME': data.name,
            'THUMBNAIL': data.thumbnail
        })
