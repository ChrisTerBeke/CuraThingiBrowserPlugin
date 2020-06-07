# Copyright (c) 2020.
# ThingiBrowser plugin is released under the terms of the LGPLv3 or higher.
from unittest.mock import patch, MagicMock, DEFAULT, call
from typing import Callable

import os
import pytest
from surrogate import surrogate


class ExtensionMock(MagicMock):

    def getPluginId(self) -> str:
        return "ThingiBrowser"

    def setMenuName(self, name: str) -> None:
        pass

    def addMenuItem(self, name: str, callback: Callable) -> None:
        pass


class TestThingiBrowserExtension:

    @pytest.fixture
    @surrogate("cura.CuraApplication.CuraApplication")
    @surrogate("UM.Extension.Extension")
    @surrogate("UM.Logger.Logger")
    @surrogate("UM.Signal.Signal")
    def make_plugin(self, application):
        with patch("cura.CuraApplication.CuraApplication", application):
            with patch("UM.Extension.Extension", ExtensionMock):
                from ..ThingiBrowser.ThingiBrowserExtension import ThingiBrowserExtension
                return ThingiBrowserExtension

    def test_extension_loads(self, make_plugin):
        with patch.multiple(ExtensionMock, setMenuName=DEFAULT, addMenuItem=DEFAULT) as mocked_values:
            plugin = make_plugin()
            mocked_values["setMenuName"].assert_called_with("ThingiBrowser")
            mocked_values["addMenuItem"].assert_has_calls([
                call("Browse", plugin.showMainWindow),
                call("Settings", plugin.showSettingsWindow)
            ])

    def test_extension_opens_main_window(self, make_plugin, application):
        application.reset_mock()
        plugin = make_plugin()
        plugin.showMainWindow()
        application.getPluginRegistry.return_value.getPluginPath.assert_called_with(plugin.getPluginId())
        application.createQmlComponent.assert_called_with("the{0}path{0}views{0}Thingiverse.qml".format(os.path.sep), {
            "ThingiService": plugin._service,
            "Analytics": plugin._analytics
        })

    def test_extension_opens_main_window_twice_only_constructs_window_once(self, make_plugin, application):
        application.reset_mock()
        plugin = make_plugin()
        plugin.showMainWindow()
        plugin.showMainWindow()
        assert len(application.createQmlComponent.mock_calls) == 1

    def test_extension_opens_settings_window(self, make_plugin, application):
        application.reset_mock()
        plugin = make_plugin()
        plugin.showSettingsWindow()
        separator = os.path.sep
        application.getPluginRegistry.return_value.getPluginPath.assert_called_with(plugin.getPluginId())
        application.createQmlComponent.assert_called_with("the{0}path{0}views{0}ThingiSettings.qml".format(separator), {
            "ThingiService": plugin._service,
            "Analytics": plugin._analytics
        })
