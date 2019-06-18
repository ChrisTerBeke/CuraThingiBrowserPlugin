// Copyright (c) 2018 Chris ter Beke.
// Thingiverse plugin is released under the terms of the LGPLv3 or higher.
import QtQuick 2.7
import QtQuick.Controls 2.2
import QtQuick.Layouts 1.3
import UM 1.1 as UM
import Cura 1.0 as Cura

ListView
{
    id: thingFilesList
    height: childrenRect.height
    width: parent.width
    interactive: false  // disable scrolling in this list
    spacing: 10
    delegate: Item
    {
        visible: modelData.name.includes(".stl") || modelData.name.includes(".STL")
        width: parent.width
        height: visible ? childrenRect.height : 0

        RowLayout
        {
            width: parent.width

            // thumbnail
            Image
            {
                Layout.leftMargin: 20
                source: modelData.thumbnail
            }

             // file name
            Label
            {
                text: modelData.name
                color: UM.Theme.getColor("text")
                font: UM.Theme.getFont("large")
                elide: Text.ElideRight
                renderType: Text.NativeRendering
                Layout.fillWidth: true
                Layout.leftMargin: 20
            }

            // download button
            Cura.PrimaryButton
            {
                text: catalog.i18nc("@button", "Add to build plate")
                onClicked: {
                    ThingiService.downloadThingFile(modelData.id)
                    Analytics.trackEvent("add_to_build_plate", "button_clicked")
                }
                Layout.rightMargin: 20
                tooltip: "Import this file onto the build plate"
            }
        }
    }
}
