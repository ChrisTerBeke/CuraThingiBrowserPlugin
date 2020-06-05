// Copyright (c) 2020.
// Thingiverse plugin is released under the terms of the LGPLv3 or higher.
import QtQuick 2.7
import QtQuick.Controls 2.2
import QtQuick.Layouts 1.3
import UM 1.1 as UM

Item
{
    width: parent.width
    height: dataRow.height
    property var thingFile: null

    RowLayout
    {
        id: dataRow
        spacing: 10
        width: parent.width

        // thumbnail (forced to 75x75)
        Image
        {
            Layout.preferredWidth: 75
            Layout.preferredHeight: 75
            fillMode: Image.PreserveAspectCrop
            clip: true
            source: thingFile.thumbnail ? thingFile.thumbnail : ""
            sourceSize.height: 75
        }

         // file name
        Label
        {
            text: thingFile.name
            color: UM.Theme.getColor("text")
            font: UM.Theme.getFont("large")
            elide: Text.ElideRight
            renderType: Text.NativeRendering
            Layout.fillWidth: true
        }

        // download button
        Button
        {
            text: "Add to build plate"
            visible: !ThingiService.isDownloading
            onClicked: {
                ThingiService.downloadThingFile(thingFile.id, thingFile.name)
                Analytics.trackEvent("add_to_build_plate", "button_clicked")
            }
        }

        // loading spinner
        AnimatedImage
        {
            visible: ThingiService.isDownloading
            source: "images/loading.gif"
        }
    }
}
