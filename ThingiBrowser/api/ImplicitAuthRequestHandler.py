# Copyright (c) 2020.
# ThingiBrowser plugin is released under the terms of the LGPLv3 or higher.
import os
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler
from typing import Dict, Any, Optional, Callable
from urllib.parse import parse_qs, urlparse, ParseResult


class ImplicitAuthRequestHandler(BaseHTTPRequestHandler):
    """
    HTTP request handler for OAuth2 implicit flow callback.
    """

    _token_callback = None  # type: Optional[Callable[[Optional[str]], None]]

    @classmethod
    def setTokenCallback(cls, callback: Callable[[Optional[str]], None]) -> None:
        """
        Set the callback function to send the received token to.
        :param callback: The callback.
        """
        cls._token_callback = callback

    def do_HEAD(self) -> None:
        self.send_response(200)

    def do_GET(self) -> None:
        parsed_url = urlparse(self.path)
        if parsed_url.path == "/callback":
            self._handleCallback(parsed_url)
        else:
            self._notFoundResponse()

    def _handleCallback(self, parsed_url: ParseResult) -> None:
        if not self._token_callback:
            self._exceptionResponse("Token callback not configured")
            return
        query = parse_qs(parsed_url.query)
        if not query:
            # The OAuth2 implicit flow returns the access_token as URL fragment, not a query parameter.
            # This response makes the JS in the served page replace the # with a ? and redirects back to /callback.
            # From there on we can parse the query and retrieve the access token.
            # This is a security feature of OAuth2 which prevents following an implicit flow from a server application.
            self._transformFragmentResponse()
            return
        access_token = self._getParam(query, "access_token")
        if not access_token:
            self._exceptionResponse("Access token could not be found in query")
            self._token_callback(None)
            return
        self._successResponse()
        self._token_callback(access_token)

    def _transformFragmentResponse(self) -> None:
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        doc = open("{}/../static/AuthenticationRedirect.html".format(os.path.dirname(__file__)), "rb")
        self.wfile.write(doc.read())

    def _successResponse(self) -> None:
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        doc = open("{}/../static/AuthenticationReceived.html".format(os.path.dirname(__file__)), "rb")
        self.wfile.write(doc.read())

    def _notFoundResponse(self) -> None:
        self.send_response(HTTPStatus.NOT_FOUND)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        self.wfile.write(b"404 - page not found")

    def _exceptionResponse(self, message: str) -> None:
        self.send_response(HTTPStatus.INTERNAL_SERVER_ERROR)
        self.send_header("Content-Type", "text/html")
        self.wfile.write(message.encode())

    @staticmethod
    def _getParam(query: Dict, key: str, default: Optional[Any] = None) -> str:
        return str(query.get(key, [default])[0])
