# Copyright (c) 2018 Chris ter Beke.
# Thingiverse plugin is released under the terms of the LGPLv3 or higher.
import json
import os


PLUGIN_JSON_PATH = os.path.join(os.path.dirname(__file__), "plugin.json")


class Settings:
    
    # The plugin version
    with open(PLUGIN_JSON_PATH, "r") as file:
        VERSION = json.load(file).get("version", "1.0.0")
    
    # Plugin name displayed in several location.
    DISPLAY_NAME = "Thingiverse"

    # Text shown in Cura's extension menu.
    MENU_TEXT = "Browse Thingiverse"
    
    # Thingiverse API options
    THINGIVERSE_API_TOKEN = "d1057e7ec3da66ac1b81f8632606ca0a"
    THINGIVERSE_API_PER_PAGE = 20

    # Plugin settings preference keys
    PREFERENCE_KEY_BASE = "thingibrowser"
    SETTINGS_USER_NAME_PREFERENCES_KEY = "{}/user_name".format(PREFERENCE_KEY_BASE)
    
    # Google Analytics API options
    ANALYTICS_ID = "UA-16646729-7"
    ANALYTICS_CLIENT_ID_PREFERENCES_KEY = "{}/client_id".format(PREFERENCE_KEY_BASE)
