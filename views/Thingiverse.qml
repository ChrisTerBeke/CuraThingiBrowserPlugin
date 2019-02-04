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

        ColumnLayout
        {
            anchors.fill: parent

            Label
            {
                id: thingiverseTitle
                text: catalog.i18nc("@title", "Thingiverse")
                font: UM.Theme.getFont("large")
                color: UM.Theme.getColor("text")
                Layout.fillWidth: true
                renderType: Text.NativeRendering
            }

            TextField
            {
                id: thingSearchField
                placeholderText: "Search for things..."
                onEditingFinished: ThingiService.search(thingSearchField.text)
            }

            ThingsList
            {
                id: thingsList
                model: ThingiService.things
                Layout.fillWidth: true
                Layout.fillHeight: true
            }
        }
    }
}
