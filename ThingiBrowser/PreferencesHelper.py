# Copyright (c) 2020 Chris ter Beke.
# Thingiverse plugin is released under the terms of the LGPLv3 or higher.
from typing import Optional

from cura.CuraApplication import CuraApplication

from ..Settings import Settings


class PreferencesHelper:
    
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
    def setSetting(cls, setting_name: str, value: str) -> None:
        """
        Store the value of a setting in Cura preferences.
        :param setting_name: The name of the setting to store.
        :param value: The new value of the setting.
        """
        preference_key = "{}/{}".format(Settings.PREFERENCE_KEY_BASE, setting_name)
        CuraApplication.getInstance().getPreferences().setValue(preference_key, setting_name)
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
