// Copyright (c) 2018 Ultimaker B.V.
// Cura is released under the terms of the LGPLv3 or higher.
import QtQuick 2.7
import QtQuick.Controls 2.1
import QtQuick.Layouts 1.3
import QtQuick.Dialogs 1.1

import UM 1.1 as UM
import Cura 1.0 as Cura

Item
{
    id: thingTile
    width: parent.width
    height: dataRow.height
    property var thing: null

    RowLayout
    {
        id: dataRow
        spacing: UM.Theme.getSize("wide_margin").width
        width: parent.width

        // thumbnail
        Image
        {
            Layout.leftMargin: 20
            source: thing.thumbnail
            sourceSize.width: 75 // 75 is the thumbnail size
            sourceSize.height: 75
        }

        ColumnLayout
        {
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
            }
        }

        // import files button
        Cura.PrimaryButton
        {
            text: catalog.i18nc("@button", "Details")
            Layout.rightMargin: 20
            onClicked: {
                switch (thing.type) {
                    case "Collection":
                        ThingiService.showCollectionDetails(thing.id)
                    case "Thing":
                        ThingiService.showThingDetails(thing.id)
                }
                Analytics.trackEvent("more_details", "button_clicked")
            }
        }
    }
}
