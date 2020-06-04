from http.server import HTTPServer
from UM.Logger import Logger  # type: ignore
from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
from typing import Dict, Any, Optional, Callable

import os
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
            self.end_headers()
            self._callback(query)
        else:
            Logger.log('i', 'Request received: {}'.format(parsed_url.path))
            try:
                self.send_response(200)
                self.send_header("Content Type", "application/octect")
                self.end_headers()
                doc = open("{}/../static{}".format(self._get_relative_path(), parsed_url.path), "rb")
                self.wfile.write(doc.read())
            except FileNotFoundError:
                self.send_response(401)
        return

    def _callback(self, query):
        if not query:
            self._callback_transform_fragment()
            return
        
        self._callback_success(query)

    def _callback_transform_fragment(self):
        doc = open("{}/../static/AuthenticationRedirect.html".format(self._get_relative_path()), "rb")
        self.wfile.write(doc.read())

    def _callback_success(self, query: Dict):
        doc = open("{}/../static/AuthenticationReceived.html".format(self._get_relative_path()), "rb")
        self.wfile.write(doc.read())
        token = ImplicitAuthRequestHandler.get_param(query, 'access_token')
        if token and self.token_received_callback is not None:
            self.token_received_callback(token)

    @staticmethod
    def get_param(query: Dict, key: str, default: Optional[Any] = None) -> Any:
        return query.get(key, [default])[0]

    def _get_relative_path(self):
        return os.path.dirname(__file__)