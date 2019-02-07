// Copyright (c) 2018 Chris ter Beke.
// Thingiverse plugin is released under the terms of the LGPLv3 or higher.
import QtQuick 2.2
import QtQuick.Controls 2.0
import QtQuick.Dialogs 1.1
import QtQuick.Layouts 1.3
import QtQuick.Window 2.2
import UM 1.1 as UM

// the popup window
Window
{
    id: thingiverse

    // window configuration
    color: UM.Theme.getColor("main_background")
    minimumWidth: Math.round(UM.Theme.getSize("modal_window_minimum").width)
    minimumHeight: Math.round(UM.Theme.getSize("modal_window_minimum").height)
    width: minimumWidth
    height: minimumHeight

    // translations
    UM.I18nCatalog
    {
        id: catalog
        name: "thingiverse"
    }

    title: catalog.i18nc("@title", "Thingiverse")

    // main window content
    Item
    {
        anchors.fill: parent

        // the search page
        ThingSearchPage
        {
            visible: !ThingiService.hasActiveThing
        }

        // the details page
        ThingDetailsPage
        {
            thing: ThingiService.activeThing
            thingFiles: ThingiService.activeThingFiles
            visible: ThingiService.hasActiveThing
        }
    }
}
