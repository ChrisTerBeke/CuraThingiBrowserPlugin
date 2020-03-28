# Copyright (c) 2020 Chris ter Beke.
# Thingiverse plugin is released under the terms of the LGPLv3 or higher.
from unittest.mock import MagicMock

import pytest


def mock_preferences_get_value(key: str) -> str:
    if key == "thingibrowser/test_setting":
        return "default"
    elif key == "thingibrowser/test_setting_stored":
        return "stored"


@pytest.fixture
def preferences():
    preferences = MagicMock()
    preferences.addPreference.return_value = None
    preferences.getValue.side_effect = mock_preferences_get_value
    return preferences


@pytest.fixture
def application(preferences):
    app = MagicMock()
    app.getPreferences.return_value = preferences
    return app
