import uuid
from urllib.parse import urlencode
from typing import Dict
import requests

from PyQt5.QtCore import pyqtSlot, QObject

from UM.Logger import Logger
from cura.CuraApplication import CuraApplication

from ..Settings import Settings


class Analytics(QObject):
    """ The analytics service connects our app to Google Analytics. """

    def __init__(self, parent = None):
        super().__init__(parent)
        application = CuraApplication.getInstance()
        self._client_id = self._getClientId()  # type: str
        self._user_agent = "{}/{}".format(application.getApplicationName(), application.getVersion())  # type: str

    @staticmethod
    def _getClientId() -> str:
        preferences = CuraApplication.getInstance().getPreferences()
        preferences.addPreference(Settings.ANALYTICS_CLIENT_ID_PREFERENCES_KEY, "")
        client_id = preferences.getValue(Settings.ANALYTICS_CLIENT_ID_PREFERENCES_KEY)
        if not client_id or client_id == "":
            client_id = str(uuid.uuid4())
            preferences.setValue(Settings.ANALYTICS_CLIENT_ID_PREFERENCES_KEY, client_id)
        return client_id

    @pyqtSlot(str, name="trackScreen")
    def trackScreen(self, screen_name: str) -> None:
        self._send({"t": "pageview", "dp": screen_name})

    @pyqtSlot(str, str, name="trackEvent")
    def trackEvent(self, category: str, event_name: str) -> None:
        self._send({"t": "event", "ec": category, "ea": event_name, "ev": 0})

    def _send(self, data: Dict[str, any]):
        params = {
            "v": 1,
            "tid": Settings.ANALYTICS_ID,
            "cid": self._client_id,
            "av": Settings.VERSION
        }
        headers = {"User-Agent": self._user_agent}
        try:
            requests.post("https://www.google-analytics.com/collect?{}".format(urlencode({**params, **data})),
                          headers=headers)
        except Exception as err:
            Logger.log("w", "Could not call Analytics API: %s", err)
