# Copyright (c) 2018 Chris ter Beke.
# Thingiverse plugin is released under the terms of the LGPLv3 or higher.
from .thingiverse.ThingiverseExtension import ThingiverseExtension


def getMetaData():
    """
    Function called when Cura want to know the metadata for a plugin to populate the Marketplace interface.
    :return: A dict containing relevant meta data. Plugin.json data is always appended automatically.
    """
    return {}


def register(app):
    """
    Main function called when Cura boots and want to load the plugin.
    :param app: The Cura application instance.
    :return: A dict containing the extension instance.
    """
    return {
        "extension": ThingiverseExtension()
    }
