from http.server import HTTPServer
from UM.Logger import Logger  # type: ignore
from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
from typing import Dict, Any, Optional, Callable

import threading


class ImplicitAuthRequestHandler(BaseHTTPRequestHandler):

    def do_HEAD(self):
        self.do_GET()

    def do_GET(self):
        parsed_url = urlparse(self.path)
        query = parse_qs(parsed_url.query)
        Logger.log('i', 'Auth Response received: {}'.format(query))

        if parsed_url.path == '/callback':
            self.send_response(200)
            self.send_header("Content Type", "text/html")
        else:
            self.send_response(401)
        self.end_headers()

        self.wfile.write(bytes("<html><body>", "utf-8"))
        
        if query:
            self._callback_success(query)
        else:
            self._callback_transform_fragment()

        self.wfile.write(bytes("</body></html>", "utf-8"))
        #self.server.shutdown()

    def _callback_transform_fragment(self):
        self.wfile.write(bytes("<script type='text/javascript'>window.location.href = window.location.href.substring(0,window.location.href.indexOf('#'))+'?'+window.location.hash.substring(1);</script>", "utf-8"))

    def _callback_success(self, query: Dict):
        self.wfile.write(bytes("<h2>Authentication Received!</h2>", "utf-8"))
        self.wfile.write(bytes("<p>You can close this tab now and return to ThingiBrowser on Cura.</p>", "utf-8"))
        token = ImplicitAuthRequestHandler.get_param(query, 'access_token')
        if token:
            self.wfile.write(bytes("<p>Token received: {}".format(token), "utf-8"))

            if self.token_received_callback is not None:
                self.token_received_callback(token)

    @staticmethod
    def get_param(query: Dict, key: str, default: Optional[Any] = None) -> Any:
        return query.get(key, [default])[0]