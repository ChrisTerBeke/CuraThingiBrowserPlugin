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

from ..Settings import Settings


class JSONObject(QObject):
    """ Simple class that converts a JSON object to a Python model. """
    def __init__(self, _dict: Dict[str, any]):
        if _dict:
            vars(self).update(_dict)
        super().__init__()


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
    def getUserCollectionsUrl(self, user_id: int) -> str:
        pass

    @abstractmethod
    def getCollectionUrl(self, collection_id: int) -> str:
        pass

    @abstractmethod
    def getLikesUrl(self, user_id: int) -> str:
        pass

    @abstractmethod
    def getUserThingsUrl(self, user_id: int) -> str:
        pass

    @abstractmethod
    def getUserMakesUrl(self, user_id: int) -> str:
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
    def downloadThingFile(self, file_id: int, on_finished: Callable[[bytes], Any]) -> None:
        """
        Download a thing file by its ID.
        :param file_id: The file ID to download.
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
        """
        pass

    def _createEmptyRequest(self, url: str, content_type: str = "application/json") -> QNetworkRequest:
        """
        Create a new network request with the needed HTTP headers.
        :param url: The full URL to do the request on.
        :return: The QNetworkRequest.
        """
        request = QNetworkRequest(QUrl().fromUserInput(url))
        request.setHeader(QNetworkRequest.ContentTypeHeader, content_type)
        request.setAttribute(QNetworkRequest.RedirectPolicyAttribute, True)  # file downloads reply with a 302 first
        if (self._auth is not None):
            request.setRawHeader(b"Authorization", self._auth)
        return request

    @staticmethod
    def _parseReply(reply: QNetworkReply) -> Tuple[int, Optional[Union[List[Any], Dict[str, Any]]]]:
        """
        Parse the given JSON network reply into a status code and JSON object.
        :param reply: The reply from the server.
        :return: A tuple with a status code and a dictionary.
        """
        status_code = reply.attribute(QNetworkRequest.HttpStatusCodeAttribute)
        try:
            response = bytes(reply.readAll()).decode()
            return status_code, json.loads(response)
        except (UnicodeDecodeError, JSONDecodeError, ValueError) as err:
            Logger.logException("e", "Could not parse the API response: %s", err)
            return status_code, None

    def _addCallback(self, reply: QNetworkReply, on_finished: Union[Callable[[JSONObject], Any],
                                                                    Callable[[List[JSONObject]], Any]],
                     on_failed: Optional[Callable[[JSONObject], Any]] = None,
                     request_url: Optional[str] = None) -> None:
        """
        Creates a callback function so that it includes the parsing of the response into the correct model.
        The callback is added to the 'finished' signal of the reply.
        :param reply: The reply that should be listened to.
        :param on_finished: The callback in case the response is successful.
        """
        def parse() -> None:
            self._anti_gc_callbacks.remove(parse)
            status_code, response = self._parseReply(reply)
            if not status_code or status_code >= 400:
                url_desc = ""
                if request_url:
                    url_desc = " for {}".format(request_url)
                Logger.log("w", "API returned status code {}{}: {}".format(status_code, url_desc, response))
                return on_failed(JSONObject(response) if response else None)
            result = [JSONObject(item) for item in response] if isinstance(response, list) else JSONObject(response)
            on_finished(result)

        self._anti_gc_callbacks.append(parse)
        reply.finished.connect(parse)
