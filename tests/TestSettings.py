# Copyright (c) 2020.
# ThingiBrowser plugin is released under the terms of the LGPLv3 or higher.
from ..ThingiBrowser.Settings import Settings


class TestSettings:

    def test_settings(self):
        assert Settings.DISPLAY_NAME == "ThingiBrowser"
        assert Settings.VERSION != "0.0.0"
