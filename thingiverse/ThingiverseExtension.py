# Copyright (c) 2018 Chris ter Beke.
# Thingiverse plugin is released under the terms of the LGPLv3 or higher.
import os
from typing import Optional

from PyQt5.QtCore import QObject

from UM.Extension import Extension
from UM.PluginRegistry import PluginRegistry
from cura.CuraApplication import CuraApplication

from ..Settings import Settings
from .ThingiverseService import ThingiverseService
from .Analytics import Analytics


class ThingiverseExtension(Extension):
    """
    Thingiverse plugin main file. Controls all UI and behaviour.
    """
    
    def __init__(self) -> None:
        super().__init__()
        
        # The API client that we do all calls to Thingiverse with.
        self._service = ThingiverseService(self)  # type: ThingiverseService
        
        # The API client that will talk to Google Analytics.
        self._analytics = Analytics()  # type: Analytics
        
        # The UI objects.
        self._main_dialog = None
        self._settings_dialog = None
               
        # Configure the 'extension' menu.
        self.setMenuName(Settings.DISPLAY_NAME)
        self.addMenuItem(Settings.MENU_TEXT, self._showMainWindow)

    def _showMainWindow(self) -> None:
        """
        Show the main popup window.
        """
        if not self._main_dialog:
            self._main_dialog = self._createDialog("Thingiverse.qml")
        self._main_dialog.show()
        self._service.updateSupportedFileTypes()
        self._service.search("ultimaker")
        self._service.loadDynamicDisplayMessage()

    def showSettingsWindow(self) -> None:
        """
        Show the settings popup window.
        """
        if not self._settings_dialog:
            self._settings_dialog = self._createDialog("ThingiSettings.qml")
        self._settings_dialog.show()

    def _createDialog(self, qml_file_path: str) -> Optional[QObject]:
        """
        Create a dialog window
        :return: The QML dialog object.
        """
        # Find the QML file in the plugin sources.
        plugin_path = PluginRegistry.getInstance().getPluginPath(self.getPluginId())
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
