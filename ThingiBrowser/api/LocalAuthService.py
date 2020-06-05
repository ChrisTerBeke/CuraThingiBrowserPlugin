# Copyright (c) 2020.
# ThingiBrowser plugin is released under the terms of the LGPLv3 or higher.
import threading
from http.server import HTTPServer
from typing import Callable, Any, Optional

from ..api.ImplicitAuthRequestHandler import ImplicitAuthRequestHandler


class LocalAuthService:
    """
    Service that organizes authentication flows with web services.
    """
    def __init__(self, token_callback: Optional[Callable[[Optional[str]], Any]] = None):
        self._token_callback = token_callback
        self._server = HTTPServer(("0.0.0.0", 55444), ImplicitAuthRequestHandler)
        self._server.RequestHandlerClass.setTokenCallback(self._onTokenReceived)
        self._server_thread = threading.Thread(None, self._server.serve_forever, daemon=True)

    def _onTokenReceived(self, token: Optional[str] = None) -> None:
        """
        Handler for when an implicit auth token was received.
        Closes the server so the port can be re-used.
        :param token: The received auth token.
        """
        if self._token_callback:
            self._token_callback(token)
        self._server.server_close()

    def listen(self) -> None:
        """
        Start the server on a new thread.
        """
        self._server_thread.start()
