# Copyright (c) 2020 Chris ter Beke.
# ThingiBrowser plugin is released under the terms of the LGPLv3 or higher.
from unittest.mock import patch, MagicMock, DEFAULT
from typing import Callable

import pytest
from surrogate import surrogate


class ExtensionMock(MagicMock):

    def setMenuName(self, name: str) -> None:
        pass

    def addMenuItem(self, name: str, callback: Callable) -> None:
        pass


class TestThingiBrowserExtension:

    @pytest.fixture
    @surrogate("cura.CuraApplication.CuraApplication")
    @surrogate("UM.Extension.Extension")
    @surrogate("UM.PluginRegistry.PluginRegistry")
    @surrogate("UM.Logger.Logger")
    def make_plugin(self, application):
        with patch("cura.CuraApplication.CuraApplication", application):
            with patch("UM.Extension.Extension", ExtensionMock):
                from ..ThingiBrowser.ThingiBrowserExtension import ThingiBrowserExtension
                return ThingiBrowserExtension

    def test_extension_loads(self, make_plugin):
        with patch.multiple(ExtensionMock, setMenuName=DEFAULT, addMenuItem=DEFAULT) as mocked_values:
            plugin = make_plugin()
            mocked_values["setMenuName"].assert_called_with("ThingiBrowser")
            mocked_values["addMenuItem"].assert_called_with("Open", plugin.showMainWindow)
