# Copyright (c) 2020 Chris ter Beke.
# ThingiBrowser plugin is released under the terms of the LGPLv3 or higher.
from unittest.mock import MagicMock

import pytest


def mock_preferences_get_value(key: str) -> str:
    """
    Mock implementation of Preferences().getValue().
    :param key: The preference key to get the value for.
    :return: The value of the preference.
    """
    if key == "thingibrowser/test_setting":
        return "default"
    elif key == "thingibrowser/test_setting_stored":
        return "stored"


@pytest.fixture(scope="session")
def preferences():
    """
    Fake preferences that mocks Cura's Preferences.
    :return: A MagicMock compatible with Cura's Preferences class.
    """
    preferences = MagicMock()
    preferences.addPreference = MagicMock(return_value=None)
    preferences.getValue = mock_preferences_get_value
    preferences.setValue = MagicMock(return_value=None)
    return preferences


@pytest.fixture(scope="session")
def application(preferences):
    """
    Fake application that mocks Cura's CuraApplication.
    :param preferences: A Preferences mock.
    :return: A MagicMock compatible with Cura's CuraApplication class.
    """
    app = MagicMock()
    app.getPreferences = MagicMock(return_value=preferences)
    app.getInstance = MagicMock(return_value=app)
    return app
