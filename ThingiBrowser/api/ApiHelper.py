# Copyright (c) 2020.
# Thingiverse plugin is released under the terms of the LGPLv3 or higher.
import json
from json import JSONDecodeError

from PyQt5.QtNetwork import QNetworkReply, QNetworkRequest
from typing import Tuple, Union, List, Dict, Any, Optional

from UM.Logger import Logger  # type: ignore


class ApiHelper:
    """ Assorted helper functions for API interaction. """

    @classmethod
    def parseReplyAsJson(cls, reply: QNetworkReply
                         ) -> Tuple[int, Optional[Union[Dict[str, Any], List[Dict[str, Any]]]]]:
        """
        Parse the given API reply into a status code and JSON object.
        :param reply: The reply from the server.
        :return: A tuple with a status code and the response body as JsonObject.
        """
        status_code = reply.attribute(QNetworkRequest.HttpStatusCodeAttribute)
        try:
            response = reply.readAll().data().decode()
            return status_code, json.loads(response)
        except (UnicodeDecodeError, JSONDecodeError, ValueError) as err:
            Logger.log("e", "Could not parse the API response: %s", err)
            return status_code, None

    @classmethod
    def parseReplyAsBytes(cls, reply: QNetworkReply) -> Tuple[int, bytes]:
        """
        Parse the given API reply into a status code and bytes.
        :param reply: The reply from the server.
        :return: A tuple with a status code and the response body as bytes.
        """
        status_code = reply.attribute(QNetworkRequest.HttpStatusCodeAttribute)
        return status_code, reply.readAll().data()
