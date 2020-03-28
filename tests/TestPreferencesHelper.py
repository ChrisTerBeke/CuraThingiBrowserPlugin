# Copyright (c) 2020 Chris ter Beke.
# ThingiBrowser plugin is released under the terms of the LGPLv3 or higher.
from unittest.mock import patch

import pytest

from surrogate import surrogate


class TestPreferencesHelper:

    @pytest.fixture
    @surrogate("cura.CuraApplication.CuraApplication")
    def preferences_helper(self, application):
        with patch("cura.CuraApplication.CuraApplication", application):
            from ..ThingiBrowser.PreferencesHelper import PreferencesHelper
            return PreferencesHelper

    def test_initSetting_returns_default_value(self, preferences_helper):
        default_value = preferences_helper.initSetting("test_setting", "default")
        assert default_value == "default"

    def test_initSetting_returns_stored_value(self, preferences_helper):
        stored_value = preferences_helper.initSetting("test_setting_stored", "default")
        assert stored_value == "stored"
