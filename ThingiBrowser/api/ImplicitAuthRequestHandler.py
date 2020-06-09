# Copyright (c) 2020.
# ThingiBrowser plugin is released under the terms of the LGPLv3 or higher.
import os
from http.server import BaseHTTPRequestHandler
from typing import Dict, Any, Optional
from urllib.parse import parse_qs, urlparse, ParseResult

from UM.Signal import Signal  # type: ignore


class ImplicitAuthRequestHandler(BaseHTTPRequestHandler):
    """
    HTTP request handler for OAuth2 implicit flow callback.
    """

    # Signal emitted with as first argument the received token.
    # We use a signal instead of a callback function in order to pass the token back to the Qt thread safely.
    onTokenReceived = Signal()

    def do_HEAD(self) -> None:
        self.do_GET()

    def do_GET(self) -> None:
        parsed_url = urlparse(self.path)
        if parsed_url.path == "/callback":
            self._handleCallback(parsed_url)
        else:
            self._notFoundResponse()

    def _handleCallback(self, parsed_url: ParseResult) -> None:
        query = parse_qs(parsed_url.query)
        if not query:
            # The OAuth2 implicit flow returns the access_token as URL fragment, not a query parameter.
            # This response makes the JS in the served page replace the # with a ? and redirects back to /callback.
            # From there on we can parse the query and retrieve the access token.
            # This is a security feature of OAuth2 which prevents following an implicit flow from a server application.
            self._htmlResponse("AuthenticationRedirect")
            return
        state = self._getParam(query, "state")
        if not state:
            self._exceptionResponse("State could not be found in query")
            return
        access_token = self._getParam(query, "access_token")
        if not access_token:
            self._exceptionResponse("Access token could not be found in query")
            return
        self._htmlResponse("AuthenticationReceived")
        self.onTokenReceived.emit(state, access_token)

    def _htmlResponse(self, page_name: str) -> None:
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        doc = open("{}/../static/{}.html".format(os.path.dirname(__file__), page_name), "rb")
        self.wfile.write(doc.read())

    def _notFoundResponse(self) -> None:
        self.send_response(404)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        self.wfile.write(b"404 - page not found")

    def _exceptionResponse(self, message: str) -> None:
        self.send_response(500)
        self.send_header("Content-Type", "text/html")
        self.wfile.write(message.encode())

    @staticmethod
    def _getParam(query: Dict, key: str, default: Optional[Any] = None) -> str:
        return str(query.get(key, [default])[0])
