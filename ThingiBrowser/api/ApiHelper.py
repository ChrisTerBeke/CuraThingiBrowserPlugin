# Copyright (c) 2020 Chris ter Beke.
# Thingiverse plugin is released under the terms of the LGPLv3 or higher.
import json
from json import JSONDecodeError

from PyQt5.QtNetwork import QNetworkReply, QNetworkRequest
from typing import Tuple, Union, List

from UM.Logger import Logger

from .JsonObject import JsonObject


class ApiHelper:
    """ Assorted helper functions for API interaction. """
    
    @classmethod
    def parseReplyAsJson(cls, reply: QNetworkReply) -> Tuple[int, Union[JsonObject, List[JsonObject]]]:
        """
        Parse the given API reply into a status code and JSON object.
        :param reply: The reply from the server.
        :return: A tuple with a status code and the response body as JsonObject.
        """
        status_code = reply.attribute(QNetworkRequest.HttpStatusCodeAttribute)
        try:
            response = bytes(reply.readAll()).decode()
            return status_code, json.loads(response)
        except (UnicodeDecodeError, JSONDecodeError, ValueError) as err:
            Logger.logException("e", "Could not parse the API response: %s", err)
            return status_code, []

    @classmethod
    def parseReplyAsBytes(cls, reply: QNetworkReply) -> Tuple[int, bytes]:
        """
        Parse the given API reply into a status code and bytes.
        :param reply: The reply from the server.
        :return: A tuple with a status code and the response body as bytes.
        """
        status_code = reply.attribute(QNetworkRequest.HttpStatusCodeAttribute)
        return status_code, bytes(reply.readAll())
