# Copyright (c) 2020.
# ThingiBrowser plugin is released under the terms of the LGPLv3 or higher.
import threading
from http.server import HTTPServer
from typing import Optional

from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QDesktopServices

from UM.Signal import Signal  # type: ignore


class LocalAuthService:
    """
    Service that organizes multiple parallel authentication flows with web services.
    """

    _server = None  # type: Optional[HTTPServer]
    _thread = None  # type: Optional[threading.Thread]

    # Signal emitted with as first argument the received token.
    # We use a signal instead of a callback function in order to pass the token back to the Qt thread safely.
    onTokenReceived = Signal()

    @classmethod
    def start(cls, url: str) -> None:
        """
        Start the server in a separate thread and open the authentication page.
        """
        if not cls._server:
            # FIXME: when importing globally this causes issues with UM.Signal.Signal in PyTest
            from ..api.ImplicitAuthRequestHandler import ImplicitAuthRequestHandler
            ImplicitAuthRequestHandler.onTokenReceived.connect(cls.onTokenReceived)
            cls._server = HTTPServer(("0.0.0.0", 55444), ImplicitAuthRequestHandler)
        if not cls._thread:
            cls._thread = threading.Thread(name="LocalAuthService", target=cls._server.serve_forever, daemon=True)
        if not cls._thread.is_alive():
            cls._thread.start()
        QDesktopServices.openUrl(QUrl(url))
