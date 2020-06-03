from ..api.AuthRequestHandler import ImplicitAuthRequestHandler
from urllib.parse import urlencode
from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import Type, Callable, Any, Dict, Optional
from ..PreferencesHelper import PreferencesHelper
import threading
from UM.Logger import Logger


class LocalAuthServer(HTTPServer):
    ##  Set the authorization callback on the request handler.
    def setTokenReceivedCallback(self, token_received_callback: Callable[[str], Any]) -> None:
        self.RequestHandlerClass.token_received_callback = token_received_callback  # type: ignore

class LocalAuthService():

    def __init__(self, preference_key: str, port: int = 8080, handler: Type["BaseHTTPRequestHandler"] = ImplicitAuthRequestHandler):
        self._server = LocalAuthServer(("0.0.0.0", port), handler)
        PreferencesHelper.initSetting(preference_key, None)
        self._preference_key = preference_key
        self._server.setTokenReceivedCallback(self._onTokenReceived)
        self._server_thread = threading.Thread(None, self._server.serve_forever, daemon = True)

    def _onTokenReceived(self, token: str):
        Logger.log('i', "Token stored: {}".format(token))
        PreferencesHelper.setSetting(self._preference_key, token)

    def listen(self):
        # Start the server on a new thread.
        self._server_thread.start()
