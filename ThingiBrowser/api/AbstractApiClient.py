# Copyright (c) 2020.
# Thingiverse plugin is released under the terms of the LGPLv3 or higher.
from typing import List, Callable, Any, Tuple, Optional
from abc import ABC, abstractmethod

from PyQt5.QtCore import QUrl
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkReply, QNetworkRequest

from UM.Logger import Logger  # type: ignore

from .ApiHelper import ApiHelper
from .JsonObject import Thing, ThingFile, Collection, ApiError


class AbstractApiClient(ABC):
    """ Client for interacting with the Thingiverse API. """

    # Re-usable network manager.
    _manager = QNetworkAccessManager()

    # Prevent auto-removing running callbacks by the Python garbage collector.
    _anti_gc_callbacks = []  # type: List[Callable[[], None]]

    @abstractmethod
    def authenticate(self) -> None:
        """
        Trigger authentication flow to store user token/authorization
        """
        raise NotImplementedError("authenticate must be implemented")

    @abstractmethod
    def clearAuthentication(self) -> None:
        """
        Clear the authentication state for this driver.
        """
        raise NotImplementedError("clearAuthentication must be implemented")

    @abstractmethod
    def getThingsFromCollectionQuery(self, collection_id: str) -> str:
        """
        Get the query that returns all things in a certain collection.
        :param collection_id: The ID of the collection.
        :return: The query.
        """
        raise NotImplementedError("getThingsFromCollectionQuery must be implemented")

    @abstractmethod
    def getThingsLikedByUserQuery(self) -> str:
        """
        Get the query that return all things liked by the currently authenticated user.
        :return: The query.
        """
        raise NotImplementedError("getThingsLikedByUserQuery must be implemented")

    @abstractmethod
    def getThingsByUserQuery(self) -> str:
        """
        Get the query that return all things uploaded by the currently authenticated user.
        :return: The query.
        """
        raise NotImplementedError("getThingsByUserQuery must be implemented")

    @abstractmethod
    def getThingsMadeByUserQuery(self) -> str:
        """
        Get the query that return all things made by the currently authenticated user.
        :return: The query.
        """
        raise NotImplementedError("getThingsMadeByUserQuery must be implemented")

    @abstractmethod
    def getPopularThingsQuery(self) -> str:
        """
        Get the query that return all popular things.
        :return: The query.
        """
        raise NotImplementedError("getPopularThingsQuery must be implemented")

    @abstractmethod
    def getFeaturedThingsQuery(self) -> str:
        """
        Get the query that return all featured things.
        :return: The query.
        """
        raise NotImplementedError("getFeaturedThingsQuery must be implemented")

    @abstractmethod
    def getNewestThingsQuery(self) -> str:
        """
        Get the query that return all newest things.
        :return: The query.
        """
        raise NotImplementedError("getNewestThingsQuery must be implemented")

    @abstractmethod
    def getThingsBySearchQuery(self, search_terms: str) -> str:
        """
        Get the query that return all things that match the given search terms.
        :return: The query.
        """
        raise NotImplementedError("getThingsBySearchQuery must be implemented")

    @abstractmethod
    def getCollections(self, on_finished: Callable[[List[Collection]], Any],
                       on_failed: Optional[Callable[[Optional[ApiError],Optional[int]], Any]]) -> None:
        """
        Get user's collections.
        :param on_finished: Callback with user's collections.
        :param on_failed: Callback with server response.
        """
        raise NotImplementedError("getCollections must be implemented")

    @abstractmethod
    def getThing(self, thing_id: int, on_finished: Callable[[Thing], Any],
                 on_failed: Optional[Callable[[Optional[ApiError],Optional[int]], Any]] = None) -> None:
        """
        Get a single thing by ID.
        :param thing_id: The thing ID.
        :param on_finished: Callback method to receive the async result on.
        :param on_failed: Callback method to receive failed request on.
        """
        raise NotImplementedError("getThing must be implemented")

    @abstractmethod
    def getThingFiles(self, thing_id: int, on_finished: Callable[[List[ThingFile]], Any],
                      on_failed: Optional[Callable[[Optional[ApiError],Optional[int]], Any]] = None) -> None:
        """
        Get a thing's files by ID.
        :param thing_id: The thing ID.
        :param on_finished: Callback method to receive the async result on.
        :param on_failed: Callback method to receive failed request on.
        """
        raise NotImplementedError("getThingFiles must be implemented")

    @abstractmethod
    def downloadThingFile(self, file_id: int, file_name: str, on_finished: Callable[[bytes], Any]) -> None:
        """
        Download a thing file by its ID.
        :param file_id: The file ID to download.
        :param file_name: The file's name including extension.
        :param on_finished: Callback method to receive the async result on as bytes.
        """
        raise NotImplementedError("downloadThingFile must be implemented")

    @abstractmethod
    def getThings(self, query: str, page: int, on_finished: Callable[[List[Thing]], Any],
                  on_failed: Optional[Callable[[Optional[ApiError],Optional[int]], Any]] = None) -> None:
        """
        Get things by query.
        :param query: The things to get.
        :param page: Page number of query results (for pagination).
        :param on_finished: Callback method to receive the async result on.
        :param on_failed: Callback method to receive failed request on.
        """
        raise NotImplementedError("get must be implemented")

    @property
    @abstractmethod
    def _root_url(self) -> str:
        """
        Get the API root URL for this provider.
        :returns: The root URL as string.
        """
        raise NotImplementedError("_root_url must be implemented")

    @abstractmethod
    def _setAuth(self, request: QNetworkRequest):
        """
        Get the API authentication method for this provider.
        """
        raise NotImplementedError("_setAuth must be implemented")

    def _createEmptyRequest(self, url: str, content_type: str = "application/json") -> QNetworkRequest:
        """
        Create a new network request with the needed HTTP headers.
        :param url: The full URL to do the request on.
        :param content_type: Content-Type header value
        :return: The QNetworkRequest.
        """
        request = QNetworkRequest(QUrl(url))
        request.setHeader(QNetworkRequest.ContentTypeHeader, content_type)
        request.setAttribute(QNetworkRequest.RedirectPolicyAttribute, True)  # file downloads reply with a 302 first
        self._setAuth(request)
        return request

    def _addCallback(self, reply: QNetworkReply,
                     on_finished: Callable[[Any], Any],
                     on_failed: Optional[Callable[[Optional[ApiError], Optional[int]], Any]] = None,
                     parser: Optional[Callable[[QNetworkReply], Tuple[int, Any]]] = None) -> None:
        """
        Creates a callback function so that it includes the parsing of the response into the correct model.
        The callback is added to the 'finished' signal of the reply.
        :param reply: The reply that should be listened to.
        :param on_finished: The callback in case the request is successful.
        :param on_failed: The callback in case the request fails.
        :param parser: A custom parser for the response data, defaults to a JSON parser.
        """
        def parse() -> None:
            self._anti_gc_callbacks.remove(parse)
            status_code, response = parser(reply) if parser else ApiHelper.parseReplyAsJson(reply)
            if not status_code or status_code >= 400 or response is None:
                Logger.warning("API returned with status {} and body {}".format(status_code, response))
                if on_failed:
                    error_response = None
                    if isinstance(response, dict):
                        error_response = ApiError(response)
                    on_failed(error_response, status_code)
            else:
                on_finished(response)
            reply.deleteLater()

        self._anti_gc_callbacks.append(parse)
        reply.finished.connect(parse)  # type: ignore
