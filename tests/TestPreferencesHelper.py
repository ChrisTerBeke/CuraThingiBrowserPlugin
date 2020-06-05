# Copyright (c) 2020.
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

    def test_getSettingValue_returns_stored_value(self, preferences_helper):
        stored_value = preferences_helper.getSettingValue("test_setting_stored")
        assert stored_value == "stored"

    def test_setSetting_stores_new_value(self, preferences_helper, preferences):
        preferences_helper.setSetting("test_setting_stored", "new_stored_value")
        preferences.setValue.assert_called_with("thingibrowser/test_setting_stored", "new_stored_value")

    def test_getAllSettings_returns_all_settings(self, preferences_helper):
        all_settings = preferences_helper.getAllSettings(drivers={}, views={})
        assert len(all_settings) == 4
