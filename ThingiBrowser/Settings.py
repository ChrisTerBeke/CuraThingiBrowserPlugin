# Copyright (c) 2020.
# ThingiBrowser plugin is released under the terms of the LGPLv3 or higher.
import json
import os


PLUGIN_JSON_PATH = os.path.join(os.path.dirname(__file__), "..", "plugin.json")


class Settings:

    # The plugin version
    with open(PLUGIN_JSON_PATH, "r") as file:
        VERSION = json.load(file).get("version", "0.0.0")

    # Plugin name displayed in several location.
    DISPLAY_NAME = "ThingiBrowser"

    # Generic API settings
    PER_PAGE = 20

    # Thingiverse API options
    THINGIVERSE_CLIENT_ID = "0ea6d714d64fa4797e07"
    THINGIVERSE_API_TOKEN = "d1057e7ec3da66ac1b81f8632606ca0a"

    # MyMiniFactory API options
    MYMINIFACTORY_CLIENT_ID = "cura_browser"
    MYMINIFACTORY_API_TOKEN = "2d137c51-edd6-4c55-a815-233757dfcc7d"

    # Plugin settings preference keys
    PREFERENCE_KEY_BASE = "thingibrowser"
    THINGIVERSE_API_TOKEN_KEY = "thingiverse_access_token"
    MYMINIFACTORY_API_TOKEN_KEY = "myminifactory_access_token"
    DEFAULT_API_CLIENT_PREFERENCES_KEY = "default_api_client"
    DEFAULT_VIEW_PREFERENCES_KEY = "default_view"

    # Google Analytics API options
    ANALYTICS_ID = "UA-16646729-7"
    ANALYTICS_CLIENT_ID_PREFERENCES_KEY = "client_id"
