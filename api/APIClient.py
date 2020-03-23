# Copyright (c) 2018 Chris ter Beke.
# Thingiverse plugin is released under the terms of the LGPLv3 or higher.
import json
from json import JSONDecodeError
from typing import List, Callable, Any, Union, Dict, Tuple, Optional, cast

from PyQt5.QtCore import QUrl, QObject
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkReply, QNetworkRequest

from UM.Logger import Logger

import abc
from abc import ABC, abstractmethod

from ..Settings import Settings # type: ignore
from ..api.JSONObject import JSONObject, Thing, ThingFile # type: ignore

class ApiClient(ABC):
    """ Client for interacting with the Thingiverse API. """

    # API constants.
    @abc.abstractproperty
    def _root_url(self):
        return "Abstract URL"
    
    @abc.abstractproperty
    def _auth(self):
        return "Abstract Authentication"

    @abc.abstractproperty
    def user_id(self):
        return None
        
    # Re-usable network manager.
    _manager = QNetworkAccessManager()

    # Prevent auto-removing running callbacks by the Python garbage collector.
    _anti_gc_callbacks = []  # type: List[Callable[[], None]]

    @abstractmethod
    def getSearchUrl(self, term: str) -> str:
        """
        Get URL path for seraching for an object
        :param term: Term to use in search
        :return: Formatted URL path
        """
        pass

    @abstractmethod
    def getUserCollections(self, on_finished: Callable[[JSONObject], Any],
                                 on_failed: Optional[Callable[[JSONObject], Any]]) -> None:
        """
        Get user's collections
        :param on_finished: Callback with user's collections
        :param on_failed: Callback with server response
        """
        pass

    @abstractmethod
    def getCollection(self, collection_id: int, on_finished: Callable[[JSONObject], Any],
                                                on_failed: Optional[Callable[[JSONObject], Any]]) -> None:
        """
        Get a specific collection's objects
        :param collection_id: ID of the collection
        :param on_finished: Callback with user's collections
        :param on_failed: Callback with server response
        """
        pass

    @abstractmethod
    def getLikesUrl(self) -> str:
        """
        Get URL path for a user's liked objects
        :return: Formatted URL path
        """
        pass

    @abstractmethod
    def getUserThingsUrl(self) -> str:
        """
        Get URL path for a user's uploaded objects
        :return: Formatted URL path
        """
        pass

    @abstractmethod
    def getUserMakesUrl(self) -> str:
        """
        Get URL path for a user's printed objects
        :return: Formatted URL path
        """
        pass

    @abstractmethod
    def getPopularUrl(self) -> str:
        """
        Get URL path for most popular objects
        :return: Formatted URL path
        """
        pass

    @abstractmethod
    def getFeaturedUrl(self) -> str:
        """
        Get URL path for featured objects
        :return: Formatted URL path
        """
        pass

    @abstractmethod
    def getNewestUrl(self) -> str:
        """
        Get URL path for the newest objects
        :return: Formatted URL path
        """
        pass

    @abstractmethod
    def getThing(self, thing_id: int, on_finished: Callable[[JSONObject], Any],
                 on_failed: Optional[Callable[[JSONObject], Any]] = None) -> None:        
        """
        Get a single thing by ID.
        :param thing_id: The thing ID.
        :param on_finished: Callback method to receive the async result on.
        :param on_failed: Callback method to receive failed request on.
        """
        pass

    @abstractmethod
    def getThingFiles(self, thing_id: int, on_finished: Callable[[List[JSONObject]], Any],
                      on_failed: Optional[Callable[[JSONObject], Any]] = None) -> None:
        """
        Get a thing's files by ID.
        :param thing_id: The thing ID.
        :param on_finished: Callback method to receive the async result on.
        :param on_failed: Callback method to receive failed request on.
        """
        pass

    @abstractmethod
    def downloadThingFile(self, file_id: int, file_name: str, on_finished: Callable[[bytes], Any]) -> None:
        """
        Download a thing file by its ID.
        :param file_id: The file ID to download.
        :param file_name: The file's name including extension
        :param on_finished: Callback method to receive the async result on as bytes.
        """
        pass

    @abstractmethod
    def get(self, query: str, page: int, on_finished: Callable[[List[JSONObject]], Any],
            on_failed: Optional[Callable[[JSONObject], Any]] = None) -> None:
        """
        Get things by query.
        :param query: The things to get.
        :param page: Page number of query results (for pagination).
        :param on_finished: Callback method to receive the async result on.
        :param on_failed: Callback method to receive failed request on.
        :param convert_response: Callback to convert the response
        """
        pass

    def _createEmptyRequest(self, url: str, content_type: str = "application/json") -> QNetworkRequest:
        """
        Create a new network request with the needed HTTP headers.
        :param url: The full URL to do the request on.
        :param content_type: Content-Type header value
        :return: The QNetworkRequest.
        """
        request = QNetworkRequest(QUrl().fromUserInput(url))
        request.setHeader(QNetworkRequest.ContentTypeHeader, content_type)
        request.setAttribute(QNetworkRequest.RedirectPolicyAttribute, True)  # file downloads reply with a 302 first
        auth_type, auth = self._auth
        if auth is not None:
            if auth_type == "Authorization":
                request.setRawHeader(b"Authorization", auth)
            else:
                operator = "&" if url.find("?") > 0 else "?"
                request.setUrl(QUrl.fromUserInput("{}{}{}".format(url, operator, auth)))
        return request

    @staticmethod
    def _parseReply(reply: QNetworkReply, json_decoder: Callable[[dict], Any]) -> Tuple[int, Union[JSONObject, List[JSONObject]]]:
        """
        Parse the given JSON network reply into a status code and JSON object.
        :param reply: The reply from the server.
        :param json_decoder: Callback that returns a python object for every json object loaded
        :return: A tuple with a status code and a dictionary.
        """
        status_code = reply.attribute(QNetworkRequest.HttpStatusCodeAttribute)
        try:
            response = bytes(reply.readAll()).decode()
            return status_code, json.loads(response, object_hook=json_decoder)
        except (UnicodeDecodeError, JSONDecodeError, ValueError) as err:
            Logger.logException("e", "Could not parse the API response: %s", err)
            return status_code, []

    def _addCallback(self, reply: QNetworkReply, on_finished: Union[Callable[[JSONObject], Any],
                                                                    Callable[[List[JSONObject]], Any]],
                     on_failed: Optional[Callable[[JSONObject], Any]] = None,
                     request_url: Optional[str] = None) -> None:
        """
        Creates a callback function so that it includes the parsing of the response into the correct model.
        The callback is added to the 'finished' signal of the reply.
        :param reply: The reply that should be listened to.
        :param on_finished: The callback in case the response is successful.
        :param request_url: URL attempted used in failure logging
        """
        def parse() -> None:
            self._anti_gc_callbacks.remove(parse)
            status_code, response = self._parseReply(reply, self._jsonDecoder)
            if not status_code or status_code >= 400 or not response:
                url_desc = ""
                if request_url:
                    url_desc = " for {}".format(request_url)
                Logger.log("w", "API returned status code {}{}: {}".format(status_code, url_desc, response))
                if on_failed:
                    return on_failed(response if response else None)
                return
            on_finished(response)

        self._anti_gc_callbacks.append(parse)
        reply.finished.connect(parse)

    @staticmethod
    def _jsonDecoder(data: dict) -> JSONObject:
        """
        Function to convert dictionary for every json object in
        responses into a python object
        :param data: dictionary of key-value pairs in JSONObject
        """
        return JSONObject(data)