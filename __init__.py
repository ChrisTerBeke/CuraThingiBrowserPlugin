# Copyright (c) 2020.
# Thingiverse plugin is released under the terms of the LGPLv3 or higher.


def getMetaData():
    """
    Function called when Cura want to know the metadata for a plugin to populate the Marketplace interface.
    :return: A dict containing relevant meta data. Plugin.json data is always appended automatically.
    """
    return {}


def register(*_args, **_kwargs):
    """
    Main function called when Cura boots and want to load the plugin.
    :return: A dict containing the extension instance.
    """
    from .ThingiBrowser.ThingiBrowserExtension import ThingiBrowserExtension
    return {
        "extension": ThingiBrowserExtension()
    }
