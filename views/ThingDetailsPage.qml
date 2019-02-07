// Copyright (c) 2018 Chris ter Beke.
// Thingiverse plugin is released under the terms of the LGPLv3 or higher.
import QtQuick 2.2
import QtQuick.Controls 2.0
import QtQuick.Dialogs 1.1
import QtQuick.Layouts 1.3
import QtQuick.Window 2.2
import UM 1.1 as UM
import Cura 1.0 as Cura


ColumnLayout
{
    id: thingDetailsPage
    anchors.fill: parent
    property var thing: null
    property var thingFiles: []

    Cura.SecondaryButton
    {
        text: catalog.i18nc("@button", "Back")
        onClicked: ThingiService.hideThingDetails()
    }

    Label
    {
        id: thingTitle
        text: thing.name
        font: UM.Theme.getFont("large")
        color: UM.Theme.getColor("text")
        Layout.fillWidth: true
        renderType: Text.NativeRendering
    }

    Label
    {
        id: thingDescription
        text: thing.description
        font: UM.Theme.getFont("small")
        color: UM.Theme.getColor("text")
        Layout.fillWidth: true
        renderType: Text.NativeRendering
    }

//    Image
//    {
//        source: thing.default_image.url
//        fillMode: Image.PreserveAspectFit
//        width: 100
//        height: 100
//    }

    ThingFilesList
    {
        id: thingFilesList
        model: thingFiles
        Layout.fillWidth: true
    }
}
