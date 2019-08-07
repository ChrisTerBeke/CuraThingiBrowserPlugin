# Copyright (c) 2018 Chris ter Beke.
# Thingiverse plugin is released under the terms of the LGPLv3 or higher.
import json
from json import JSONDecodeError
from typing import List, Callable, Any, Union, Dict, Tuple, Optional, cast

from PyQt5.QtCore import QUrl, QObject
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkReply, QNetworkRequest

from UM.Logger import Logger

from ..Settings import Settings


class JSONObject(QObject):
    """ Simple class that converts a JSON object to a Python model. """
    def __init__(self, _dict: Dict[str, any]):
        if _dict:
            vars(self).update(_dict)
        super().__init__()


class ThingiverseApiClient:
    """ Client for interacting with the Thingiverse API. """

    # API constants.
    _root_url = "https://api.thingiverse.com"
    _token = Settings.THINGIVERSE_API_TOKEN

    # Re-usable network manager.
    _manager = QNetworkAccessManager()

    # Prevent auto-removing running callbacks by the Python garbage collector.
    _anti_gc_callbacks = []  # type: List[Callable[[], None]]

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
        self._addCallback(reply, on_finished, on_failed)

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
        self._addCallback(reply, on_finished, on_failed)

    def downloadThingFile(self, file_id: int, on_finished: Callable[[bytes], Any]) -> None:
        """
        Download a thing file by its ID.
        :param file_id: The file ID to download.
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

    def search(self, search_terms: str, on_finished: Callable[[List[JSONObject]], Any],
               on_failed: Optional[Callable[[JSONObject], Any]] = None, page: int = 1) -> None:
        """
        Get things by searching.
        :param page: Page of search results.
        :param search_terms: The terms to search with.
        :param on_finished: Callback method to receive the async result on.
        :param on_failed: Callback method to receive failed request on.
        """
        url = "{}/search/{}?per_page={}&page={}".format(
                self._root_url, search_terms, Settings.THINGIVERSE_API_PER_PAGE, page)
        reply = self._manager.get(self._createEmptyRequest(url))
        self._addCallback(reply, on_finished, on_failed)

    def _createEmptyRequest(self, url: str, content_type: str = "application/json") -> QNetworkRequest:
        """
        Create a new network request with the needed HTTP headers.
        :param url: The full URL to do the request on.
        :return: The QNetworkRequest.
        """
        request = QNetworkRequest(QUrl().fromUserInput(url))
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
            Logger.logException("e", "Could not parse the API response: %s", err)
            return status_code, None

    def _addCallback(self, reply: QNetworkReply, on_finished: Union[Callable[[JSONObject], Any],
                                                                    Callable[[List[JSONObject]], Any]],
                     on_failed: Optional[Callable[[JSONObject], Any]] = None) -> None:
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
                Logger.log("w", "API returned status code {}: {}".format(status_code, response))
                return on_failed(JSONObject(response) if response else None)
            result = [JSONObject(item) for item in response] if isinstance(response, list) else JSONObject(response)
            on_finished(result)

        self._anti_gc_callbacks.append(parse)
        reply.finished.connect(parse)
