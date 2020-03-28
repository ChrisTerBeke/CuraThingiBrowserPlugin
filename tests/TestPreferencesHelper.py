# Copyright (c) 2020 Chris ter Beke.
# Thingiverse plugin is released under the terms of the LGPLv3 or higher.
from unittest.mock import patch, MagicMock

from ThingiBrowser.PreferencesHelper import PreferencesHelper


class TestPreferencesHelper:

    def test_initSetting_returns_default_value(self, application):
        with patch("cura.CuraApplication.CuraApplication.getInstance", MagicMock(return_value=application)):
            default_value = PreferencesHelper.initSetting("test_setting", "default")
        assert default_value == "default"

    def test_initSetting_returns_stored_value(self, application):
        with patch("cura.CuraApplication.CuraApplication.getInstance", MagicMock(return_value=application)):
            stored_value = PreferencesHelper.initSetting("test_setting_stored", "default")
        assert stored_value == "stored"
