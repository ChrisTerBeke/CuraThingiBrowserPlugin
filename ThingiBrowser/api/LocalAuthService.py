# Copyright (c) 2020.
# ThingiBrowser plugin is released under the terms of the LGPLv3 or higher.
import threading
from http.server import HTTPServer
from typing import Optional

from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QDesktopServices

from UM.Signal import Signal  # type: ignore

from ..api.ImplicitAuthRequestHandler import ImplicitAuthRequestHandler


class LocalAuthService:
    """
    Service that organizes authentication flows with web services.
    """

    # Signal emitted with as first argument the received token.
    # We use a signal instead of a callback function in order to pass the token back to the Qt thread safely.
    onTokenReceived = Signal()

    _server = HTTPServer(("0.0.0.0", 55444), ImplicitAuthRequestHandler)
    _thread = threading.Thread(name="LocalAuthService", target=_server.serve_forever, daemon=True)

    def start(self, url: str) -> None:
        """
        Start the server in a separate thread and open the authentication page.
        """
        if not self._thread.isAlive():
            # Only start the thread once. From the first use onward we keep it running.
            self._thread.start()
        ImplicitAuthRequestHandler.onTokenReceived.connect(self._onTokenReceived)
        QDesktopServices.openUrl(QUrl(url))

    def _onTokenReceived(self, token: Optional[str] = None) -> None:
        """
        Handler for when an implicit auth token was received.
        Closes the server so the port can be re-used.
        :param token: The received auth token.
        """
        ImplicitAuthRequestHandler.onTokenReceived.disconnect(self._onTokenReceived)
        self.onTokenReceived.emit(token)
        # FIXME: Figure out how to stop the server and join the thread without blocking Cura for a while
