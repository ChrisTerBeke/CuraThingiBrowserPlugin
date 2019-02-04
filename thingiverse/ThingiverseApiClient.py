# Copyright (c) 2018 Chris ter Beke.
# Thingiverse plugin is released under the terms of the LGPLv3 or higher.
import json
from json import JSONDecodeError
from typing import List, Callable, Any, Union, TypeVar, Type, Dict, Tuple, Optional, cast

from PyQt5.QtCore import QUrl
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkReply, QNetworkRequest

from UM.Logger import Logger

from .Thing import Thing


## The generic type variable used to document the methods below.
ThingiverseApiClientModel = TypeVar("ThingiverseApiClientModel", bound = Thing)


class ThingiverseApiClient:
    """
    Client for interacting with the Thingiverse API.
    """
    
    # API constants.
    _root_url = "https://api.thingiverse.com"
    _download_root_url = "https://www.thingiverse.com/download"
    _token = "d1057e7ec3da66ac1b81f8632606ca0a"
    
    def __init__(self) -> None:
        
        # Re-usable network manager.
        self._manager = QNetworkAccessManager()
        
        # Prevent auto-removing running callbacks by the Python garbage collector.
        self._anti_gc_callbacks = []  # type: List[Callable[[], None]]
        
    def download(self, thing_id: int, on_finished: Callable[[bytes], Any]) -> None:
        """
        Download a thing by it's download URL.
        :param thing_id: The thing ID to download.
        :param on_finished: Callback method to receive the async result on as bytes.
        """
        # TODO: we actually need to get the thing's API info first as that points to one or more files.
        # TODO: this results in a chain of API calls and responses: thing -> thing files -> download(s)
        url = "{}:{}".format(self._download_root_url, str(thing_id))
        reply = self._manager.get(self._createEmptyRequest(url, "plain/text"))
        self._addSimpleCallback(reply, on_finished)
    
    def search(self, search_terms: str, on_finished: Callable[[List[Thing]], Any]) -> None:
        """
        Get things by searching.
        :param search_terms: The terms to search with.
        :param on_finished: Callback method to receive the async result on.
        """
        url = "{}/search/{}".format(self._root_url, search_terms)
        reply = self._manager.get(self._createEmptyRequest(url))
        self._addCallback(reply, on_finished, Thing)

    def _createEmptyRequest(self, url: str, content_type: str = "application/json") -> QNetworkRequest:
        """
        Create a new network request with the needed HTTP headers.
        :param url: The full URL to do the request on.
        :return: The QNetworkRequest.
        """
        request = QNetworkRequest(QUrl(url))
        request.setHeader(QNetworkRequest.ContentTypeHeader, content_type)
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
    def _parseModels(data: Dict[str, Any],
                     on_finished: Union[Callable[[ThingiverseApiClientModel], Any],
                                        Callable[[List[ThingiverseApiClientModel]], Any]],
                     model_class: Type[ThingiverseApiClientModel]) -> None:
        """
        Parse the API response into a model instance or list of instances.
        :param data: The JSON data from the server.
        :param on_finished: The callback in case the response is successful.
        :param model_class: The type of the model to convert the response to.
        :return:
        """
        if isinstance(data, list):
            results = [model_class(**c) for c in data]  # type: List[ThingiverseApiClientModel]
            on_finished_list = cast(Callable[[List[ThingiverseApiClientModel]], Any], on_finished)
            on_finished_list(results)
        else:
            result = model_class(**data)  # type: ThingiverseApiClientModel
            on_finished_item = cast(Callable[[ThingiverseApiClientModel], Any], on_finished)
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
    
    def _addCallback(self,
                     reply: QNetworkReply,
                     on_finished: Union[Callable[[ThingiverseApiClientModel], Any],
                                        Callable[[List[ThingiverseApiClientModel]], Any]],
                     model: Type[ThingiverseApiClientModel] = None) -> None:
        """
        Creates a callback function so that it includes the parsing of the response into the correct model.
        The callback is added to the 'finished' signal of the reply.
        :param reply: The reply that should be listened to.
        :param on_finished: The callback in case the response is successful.
        :param model: The type of the model to convert the response to.
        """
        def parse() -> None:
            status_code, response = self._parseReply(reply)
            self._anti_gc_callbacks.remove(parse)
            return self._parseModels(response, on_finished, model)

        self._anti_gc_callbacks.append(parse)
        reply.finished.connect(parse)
