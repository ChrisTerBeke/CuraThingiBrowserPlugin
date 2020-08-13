// Copyright (c) 2020.
// Thingiverse plugin is released under the terms of the LGPLv3 or higher.
import QtQuick 2.7
import QtQuick.Controls 2.1
import QtQuick.Layouts 1.3
import QtQuick.Dialogs 1.1
import UM 1.1 as UM

Item
{
    width: parent.width
    height: dataRow.height
    property var thing: null

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
            Layout.leftMargin: 20
            fillMode: Image.PreserveAspectCrop
            clip: true
            source: thing.thumbnail ? thing.thumbnail : ""
            sourceSize.height: 75
        }

        ColumnLayout
        {
            Layout.fillWidth: true
            Layout.maximumWidth: parent.width * 0.7

            // thing title
            Label
            {
                text: thing.name
                color: UM.Theme.getColor("text")
                font: UM.Theme.getFont("large")
                elide: Text.ElideRight
                renderType: Text.NativeRendering
                Layout.fillWidth: true
            }

            // link to web page
            Link
            {
                text: thing.url
                url: thing.url
                visible: thing.url
                elide: Text.ElideRight
                Layout.fillWidth: true
            }
        }

        // details button
        Button
        {
            text: "Details"
            Layout.rightMargin: 20
            onClicked: {
                switch (thing.type) {
                    case "Collection":
                        ThingiService.showCollectionDetails(thing.id)
                        break
                    case "Thing":
                        ThingiService.showThingDetails(thing.id)
                        break
                }
                Analytics.trackEvent("more_details", "button_clicked")
            }
        }
    }
}
