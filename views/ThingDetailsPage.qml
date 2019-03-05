// Copyright (c) 2018 Chris ter Beke.
// Thingiverse plugin is released under the terms of the LGPLv3 or higher.
import QtQuick 2.2
import QtQuick.Controls 2.2
import QtQuick.Dialogs 1.1
import QtQuick.Layouts 1.3
import QtQuick.Window 2.2
import UM 1.1 as UM
import Cura 1.0 as Cura

ColumnLayout
{
    id: detailsPage

    // the active thing
    property var thing: null

    // the files for the active thing
    property var thingFiles: []

    // button to navigate back to the search results page
    Cura.SecondaryButton
    {
        text: catalog.i18nc("@button", "Back to results")
        onClicked: ThingiService.hideThingDetails()
        Layout.leftMargin: 20
        Layout.topMargin: 10
        Layout.bottomMargin: 10
    }

    Label
    {
        id: thingTitle
        text: thing.name
        font: UM.Theme.getFont("large")
        color: UM.Theme.getColor("text")
        renderType: Text.NativeRendering
        Layout.leftMargin: 20
        Layout.bottomMargin: 20
    }

    ScrollView
    {
        id: scroller
        width: detailsPage.width
        clip: true
        Layout.fillHeight: true

        Column
        {
            Label
            {
                id: thingDescription
                text: thing.description
                font: UM.Theme.getFont("small")
                color: UM.Theme.getColor("text")
                renderType: Text.NativeRendering
                wrapMode: Label.WordWrap
                width: detailsPage.width
                leftPadding: 20
                bottomPadding: 20
            }

            Label
            {
                text: "Files"
                font: UM.Theme.getFont("large")
                color: UM.Theme.getColor("text")
                renderType: Text.NativeRendering
                leftPadding: 20
                bottomPadding: 20
            }

            ThingFilesList
            {
                id: thingFilesList
                model: thingFiles
            }
        }
    }
}
