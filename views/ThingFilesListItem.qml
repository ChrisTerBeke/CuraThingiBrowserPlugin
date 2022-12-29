// Copyright (c) 2020.
// Thingiverse plugin is released under the terms of the LGPLv3 or higher.
import QtQuick 2.7
import QtQuick.Controls 2.2
import QtQuick.Layouts 1.3
import UM 1.1 as UM

Item {
    width: parent.width
    height: dataRow.height
    property var thingFile: null

    RowLayout {
        id: dataRow
        spacing: 10
        width: parent.width

        Image {
            Layout.preferredWidth: 75
            Layout.preferredHeight: 75
            fillMode: Image.PreserveAspectCrop
            clip: true
            source: thingFile.thumbnail ? thingFile.thumbnail : ""
            sourceSize.height: 75
        }

        Label {
            text: thingFile.name
            color: UM.Theme.getColor("text")
            font: UM.Theme.getFont("large")
            elide: Text.ElideRight
            renderType: Text.NativeRendering
            Layout.fillWidth: true
        }

        EnhancedButton {
            text: "Add to build plate"
            enabled: !ThingiService.isDownloading && thingFile.download_url
            // FIXME: automatically update after signing in

            onClicked: {
                ThingiService.downloadThingFile(thingFile.download_url, thingFile.name)
                Analytics.trackEvent("add_to_build_plate", "button_clicked")
            }
        }

        Label {
            text: "Please sign in to download files"
            visible: !thingFile.download_url
            color: UM.Theme.getColor("text")
            font: UM.Theme.getFont("large")
            elide: Text.ElideRight
            renderType: Text.NativeRendering
        }

        AnimatedImage {
            visible: ThingiService.isDownloading
            source: "images/loading.gif"
        }
    }
}
