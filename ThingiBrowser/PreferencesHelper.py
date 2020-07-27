# Copyright (c) 2020.
# Thingiverse plugin is released under the terms of the LGPLv3 or higher.
from typing import Optional, Dict, List, Any, Callable

from cura.CuraApplication import CuraApplication  # type: ignore

from .Settings import Settings


class PreferencesHelper:
    """
    Assorted helper functions around Cura's Preferences class.
    """

    @classmethod
    def initSetting(cls, setting_name: str, default_value: Optional[str] = "") -> str:
        """
        Initialize plugin settings in Cura's preferences.
        :param setting_name: Setting name.
        :param default_value: Setting default value.
        :return: Setting value (or default value).
        """
        preference_key = "{}/{}".format(Settings.PREFERENCE_KEY_BASE, setting_name)
        preferences = CuraApplication.getInstance().getPreferences()
        preferences.addPreference(preference_key, default_value)
        return preferences.getValue(preference_key)

    @classmethod
    def getAllSettings(cls, drivers: Dict[str, str], views: Dict[str, str]) -> List[Dict[str, Any]]:
        """
        Get all settings as key:value dict.
        :param drivers: The available drivers.
        :param views: The available views.
        :return: The settings dict.
        """
        return [
            # FIXME: Waiting for Thingiverse app approval
            # {
            #     "type": "cta_button",
            #     "key": Settings.THINGIVERSE_API_TOKEN_KEY,
            #     "value": cls.getSettingValue(Settings.THINGIVERSE_API_TOKEN_KEY),
            #     "label": "Thingiverse Account",
            #     "driver": "thingiverse"
            # },
            {
                "type": "cta_button",
                "key": Settings.MYMINIFACTORY_API_TOKEN_KEY,
                "value": cls.getSettingValue(Settings.MYMINIFACTORY_API_TOKEN_KEY),
                "label": "MyMiniFactory Account",
                "driver": "myminifactory",
                "description": "Sign in with your MyMiniFactory account to see your own likes and makes in the plugin."
            },
            {
                "type": "text",
                "key": Settings.THINGIVERSE_USER_NAME_PREFERENCES_KEY,
                "value": cls.getSettingValue(Settings.THINGIVERSE_USER_NAME_PREFERENCES_KEY),
                "label": "Thingiverse username",
                "description": "The username of the Thingiverse account to show likes and makes for. "
                               "Thingiverse is no longer actively maintained so the improved sign in flow as used for "
                               "MyMiniFactory cannot be implemented for Thingiverse."
            },
            {
                "type": "combobox",
                "key": Settings.DEFAULT_API_CLIENT_PREFERENCES_KEY,
                "value": cls.getSettingValue(Settings.DEFAULT_API_CLIENT_PREFERENCES_KEY),
                "label": "Default repository service",
                "options": drivers,
                "description": "Which 3D file repository to use when the plugin starts."
            },
            {
                "type": "combobox",
                "key": Settings.DEFAULT_VIEW_PREFERENCES_KEY,
                "value": cls.getSettingValue(Settings.DEFAULT_VIEW_PREFERENCES_KEY),
                "label": "Default view",
                "options": views,
                "description": "Which view to use when the plugin starts."
            }
        ]

    @classmethod
    def setSetting(cls, setting_name: str, value: str) -> None:
        """
        Store the value of a setting in Cura preferences.
        :param setting_name: The name of the setting to store.
        :param value: The new value of the setting.
        """
        preference_key = "{}/{}".format(Settings.PREFERENCE_KEY_BASE, setting_name)
        CuraApplication.getInstance().getPreferences().setValue(preference_key, value)

    @classmethod
    def getSettingValue(cls, setting_name: str) -> str:
        """
        Get the value of a setting from Cura preferences.
        :param setting_name: The name of the setting to get the value for.
        :return: The value of the setting.
        """
        preference_key = "{}/{}".format(Settings.PREFERENCE_KEY_BASE, setting_name)
        return CuraApplication.getInstance().getPreferences().getValue(preference_key)

    @classmethod
    def addSettingChangedCallback(cls, callback: Callable[[str], None]) -> None:
        """
        Add a callback on for the change of a preference value.
        :param callback: The callback function to run when setting is changed.
        """
        CuraApplication.getInstance().getPreferences().preferenceChanged.connect(callback)
