# Copyright (c) 2020.
# Thingiverse plugin is released under the terms of the LGPLv3 or higher.
import os
from typing import Optional

from PyQt5.QtCore import QObject
from PyQt5.QtQuick import QQuickWindow  # type: ignore

from UM.Extension import Extension  # type: ignore
from cura.CuraApplication import CuraApplication  # type: ignore

from .Settings import Settings
from .ThingiBrowserService import ThingiBrowserService
from .api.Analytics import Analytics


class ThingiBrowserExtension(Extension):
    """
    Thingiverse plugin main file. Controls all UI and behaviour.
    """

    def __init__(self) -> None:
        super().__init__()

        # The API client that we do all calls to Thingiverse with.
        self._service = ThingiBrowserService(self)  # type: ThingiBrowserService

        # The API client that will talk to Google Analytics.
        self._analytics = Analytics()  # type: Analytics

        # The UI objects.
        self._main_dialog = None  # type: Optional[QQuickWindow]
        self._settings_dialog = None  # type: Optional[QQuickWindow]

        # Configure the 'extension' menu.
        self.setMenuName(Settings.DISPLAY_NAME)
        self.addMenuItem("Browse", self.showMainWindow)
        self.addMenuItem("Settings", self.showSettingsWindow)

    def showMainWindow(self) -> None:
        """
        Show the main popup window.
        """
        if not self._main_dialog:
            self._main_dialog = self._createComponent("Thingiverse.qml")
        if self._main_dialog and isinstance(self._main_dialog, QQuickWindow):
            self._main_dialog.closing.connect(self._onClosingMainWindow)
            self._main_dialog.show()
            self._service.updateSupportedFileTypes()
            self._service.runDefaultQuery()

    def _onClosingMainWindow(self) -> None:
        """
        Actions to run when main window is closing
        """
        if self._settings_dialog:
            self._settings_dialog.close()
        self._service.resetActiveDriver()

    def showSettingsWindow(self) -> None:
        """
        Show the settings popup window.
        """
        if not self._settings_dialog:
            self._settings_dialog = self._createComponent("ThingiSettings.qml")
        if self._settings_dialog and isinstance(self._settings_dialog, QQuickWindow):
            self._settings_dialog.show()

    def _createComponent(self, qml_file_path: str) -> Optional[QObject]:
        """
        Create a dialog window
        :return: The QML dialog object.
        """
        # Find the QML file in the plugin sources.
        plugin_path = CuraApplication.getInstance().getPluginRegistry().getPluginPath(self.getPluginId())
        if not plugin_path:
            return None
        path = os.path.join(plugin_path, "views", qml_file_path)
        # Create the dialog component from a QML file.
        dialog = CuraApplication.getInstance().createQmlComponent(path, {
            "ThingiService": self._service,
            "Analytics": self._analytics
        })
        if not dialog:
            raise Exception("Failed to create Thingiverse dialog")
        return dialog
