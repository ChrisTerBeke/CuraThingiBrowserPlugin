# Copyright (c) 2018 Chris ter Beke.
# Thingiverse plugin is released under the terms of the LGPLv3 or higher.
import json
from json import JSONDecodeError
from typing import List, Callable, Any, Union, Dict, Tuple, Optional, cast

from PyQt5.QtCore import QUrl, QObject
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkReply, QNetworkRequest

from UM.Logger import Logger


class JSONObject(QObject):
    """ Simple class that converts a JSON object to a Python model. """
    def __init__(self, _dict: Dict[str, any]):
        vars(self).update(_dict)
        super().__init__()


class ThingiverseApiClient:
    """ Client for interacting with the Thingiverse API. """
    
    # API constants.
    _root_url = "https://api.thingiverse.com"
    _token = "d1057e7ec3da66ac1b81f8632606ca0a"
    
    def __init__(self) -> None:
        
        # Re-usable network manager.
        self._manager = QNetworkAccessManager()
        
        # Prevent auto-removing running callbacks by the Python garbage collector.
        self._anti_gc_callbacks = []  # type: List[Callable[[], None]]

    def getThing(self, thing_id: int, on_finished: Callable[[JSONObject], Any]) -> None:
        """
        Get a single thing by ID.
        :param thing_id: The thing ID.
        :param on_finished: Callback method to receive the async result on.
        """
        url = "{}/things/{}".format(self._root_url, thing_id)
        reply = self._manager.get(self._createEmptyRequest(url))
        self._addCallback(reply, on_finished)
        
    def getThingFiles(self, thing_id: int, on_finished: Callable[[List[JSONObject]], Any]) -> None:
        """
        Get a thing's files by ID.
        :param thing_id: The thing ID.
        :param on_finished: Callback method to receive the async result on.
        """
        url = "{}/things/{}/files".format(self._root_url, thing_id)
        reply = self._manager.get(self._createEmptyRequest(url))
        self._addCallback(reply, on_finished)
        
    def downloadThingFile(self, file_id: int, on_finished: Callable[[bytes], Any]) -> None:
        """
        Download a thing file by its ID.
        :param file_id: The file ID to download.
        :param on_finished: Callback method to receive the async result on as bytes.
        """
        url = "{}/files/{}/download".format(self._root_url, file_id)
        reply = self._manager.get(self._createEmptyRequest(url))
        self._addSimpleCallback(reply, on_finished)
    
    def search(self, search_terms: str, on_finished: Callable[[List[JSONObject]], Any]) -> None:
        """
        Get things by searching.
        :param search_terms: The terms to search with.
        :param on_finished: Callback method to receive the async result on.
        """
        url = "{}/search/{}".format(self._root_url, search_terms)
        reply = self._manager.get(self._createEmptyRequest(url))
        self._addCallback(reply, on_finished)

    def _createEmptyRequest(self, url: str, content_type: str = "application/json") -> QNetworkRequest:
        """
        Create a new network request with the needed HTTP headers.
        :param url: The full URL to do the request on.
        :return: The QNetworkRequest.
        """
        request = QNetworkRequest(QUrl(url))
        request.setHeader(QNetworkRequest.ContentTypeHeader, content_type)
        request.setAttribute(QNetworkRequest.RedirectPolicyAttribute, True)  # file downloads reply with a 302 first
        request.setRawHeader(b"Authorization", "Bearer {}".format(self._token).encode())
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
            Logger.logException("e", "Could not parse the stardust response: %s", err)
            return status_code, None
    
    @staticmethod
    def _parseModels(data: Dict[str, Any], on_finished: Union[Callable[[JSONObject], Any],
                                                              Callable[[List[JSONObject]], Any]]) -> None:
        """
        Parse the API response into a model instance or list of instances.
        :param data: The JSON data from the server.
        :param on_finished: The callback in case the response is successful.
        """
        if isinstance(data, list):
            results = [JSONObject(item) for item in data]
            on_finished_list = cast(Callable[[List[JSONObject]], Any], on_finished)
            on_finished_list(results)
        else:
            result = JSONObject(data)
            on_finished_item = cast(Callable[[JSONObject], Any], on_finished)
            on_finished_item(result)
            
    def _addSimpleCallback(self, reply: QNetworkReply, on_finished: Callable[[bytes], Any]) -> None:
        """
        Creates a callback function so that it returns the body as bytes in the callback.
        :param reply: The reply that should be listened to.
        :param on_finished: The callback in case the response is successful.
        """
        def parse() -> None:
            result = bytes(reply.readAll())
            self._anti_gc_callbacks.remove(parse)
            on_finished_cast = cast(Callable[[bytes], Any], on_finished)
            on_finished_cast(result)
        
        self._anti_gc_callbacks.append(parse)
        reply.finished.connect(parse)
    
    def _addCallback(self, reply: QNetworkReply, on_finished: Union[Callable[[JSONObject], Any],
                                                                    Callable[[List[JSONObject]], Any]]) -> None:
        """
        Creates a callback function so that it includes the parsing of the response into the correct model.
        The callback is added to the 'finished' signal of the reply.
        :param reply: The reply that should be listened to.
        :param on_finished: The callback in case the response is successful.
        """
        def parse() -> None:
            status_code, response = self._parseReply(reply)
            self._anti_gc_callbacks.remove(parse)
            return self._parseModels(response, on_finished)

        self._anti_gc_callbacks.append(parse)
        reply.finished.connect(parse)
