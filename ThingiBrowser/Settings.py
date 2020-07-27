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
    THINGIVERSE_USER_NAME_PREFERENCES_KEY = "user_name"
    # FIXME: Waiting for Thingiverse app approval
    THINGIVERSE_CLIENT_ID = ""
    THINGIVERSE_API_TOKEN = "96f45d208a4b1d99bff728038162b354"  # for public endpoints

    # MyMiniFactory API options
    MYMINIFACTORY_CLIENT_ID = "cura_thingibrowser"
    MYMINIFACTORY_API_TOKEN = "c2a3f10b-19fc-53af-5a70-b837c23ff0c5"  # for public endpoints

    # Plugin settings preference keys
    PREFERENCE_KEY_BASE = "thingibrowser"
    THINGIVERSE_API_TOKEN_KEY = "thingiverse_access_token"
    MYMINIFACTORY_API_TOKEN_KEY = "myminifactory_access_token"
    DEFAULT_API_CLIENT_PREFERENCES_KEY = "default_api_client"
    DEFAULT_VIEW_PREFERENCES_KEY = "default_view"

    # Google Analytics API options
    ANALYTICS_ID = "UA-16646729-7"
    ANALYTICS_CLIENT_ID_PREFERENCES_KEY = "client_id"
