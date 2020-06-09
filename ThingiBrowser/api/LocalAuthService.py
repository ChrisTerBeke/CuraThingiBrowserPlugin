# Copyright (c) 2020.
# ThingiBrowser plugin is released under the terms of the LGPLv3 or higher.
import threading
from http.server import HTTPServer

from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QDesktopServices

from UM.Signal import Signal  # type: ignore

from ..api.ImplicitAuthRequestHandler import ImplicitAuthRequestHandler


# We have a 'global' server and thread that we can re-use.
_server = HTTPServer(("0.0.0.0", 55444), ImplicitAuthRequestHandler)
_thread = threading.Thread(name="LocalAuthService", target=_server.serve_forever, daemon=True)


class LocalAuthService:
    """
    Service that organizes multiple parallel authentication flows with web services.
    """

    # Signal emitted with as first argument the received token.
    # We use a signal instead of a callback function in order to pass the token back to the Qt thread safely.
    onTokenReceived = Signal()

    @staticmethod
    def start(url: str) -> None:
        """
        Start the server in a separate thread and open the authentication page.
        """
        if not _thread.is_alive():
            _thread.start()
        QDesktopServices.openUrl(QUrl(url))


ImplicitAuthRequestHandler.onTokenReceived.connect(LocalAuthService.onTokenReceived)
