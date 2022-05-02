# Copyright (c) 2020.
# ThingiBrowser plugin is released under the terms of the LGPLv3 or higher.
import os
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
def plugin_registry():
    """
    Fake plugin registry that mocks Cura's PluginRegistry.
    :return: A MagicMock compatible with Cura's PluginRegistry class.
    """
    plugin_registry = MagicMock()
    plugin_registry.getPluginPath = MagicMock(return_value="the{0}path".format(os.path.sep))
    return plugin_registry


@pytest.fixture(scope="session")
def application(preferences, plugin_registry):
    """
    Fake application that mocks Cura's CuraApplication.
    :param preferences: A Preferences mock.
    :param plugin_registry: A PluginRegistry mock.
    :return: A MagicMock compatible with Cura's CuraApplication class.
    """
    app = MagicMock()
    app.getInstance = MagicMock(return_value=app)
    app.getPreferences = MagicMock(return_value=preferences)
    app.getPluginRegistry = MagicMock(return_value=plugin_registry)
    app.createQmlComponent = MagicMock(return_value=object)
    return app
