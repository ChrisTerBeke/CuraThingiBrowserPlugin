# Copyright (c) 2020.
# Thingiverse plugin is released under the terms of the LGPLv3 or higher.
import uuid
from urllib.parse import urlencode
from typing import Dict, Any

import requests
from PyQt5.QtCore import pyqtSlot, QObject

from UM.Logger import Logger  # type: ignore
from cura.CuraApplication import CuraApplication  # type: ignore

from ..PreferencesHelper import PreferencesHelper
from ..Settings import Settings


class Analytics(QObject):
    """ The analytics service connects our app to Google Analytics. """

    def __init__(self, parent = None):
        super().__init__(parent)
        application = CuraApplication.getInstance()
        self._client_id = PreferencesHelper.initSetting(Settings.ANALYTICS_CLIENT_ID_PREFERENCES_KEY, str(uuid.uuid4()))
        self._user_agent = "{}/{}".format(application.getApplicationName(), application.getVersion())

    @pyqtSlot(str, name="trackScreen")
    def trackScreen(self, screen_name: str) -> None:
        self._send({"t": "pageview", "dp": screen_name})

    @pyqtSlot(str, str, name="trackEvent")
    def trackEvent(self, category: str, event_name: str) -> None:
        self._send({"t": "event", "ec": category, "ea": event_name, "ev": 0})

    def _send(self, data: Dict[str, Any]):
        params = {
            "v": 1,
            "tid": Settings.ANALYTICS_ID,
            "cid": self._client_id,
            "av": Settings.VERSION,
            "an": "ThingiVerse plugin"
        }
        headers = {"User-Agent": self._user_agent}
        url = "https://www.google-analytics.com/collect?{}".format(urlencode({**params, **data}))
        try:
            requests.post(url, headers=headers)
        except Exception as err:
            Logger.log("w", "Could not call Analytics API: %s", err)
