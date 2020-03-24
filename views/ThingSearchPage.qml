// Copyright (c) 2020 Chris ter Beke.
// Thingiverse plugin is released under the terms of the LGPLv3 or higher.
import QtQuick 2.2
import QtQuick.Controls 2.3
import QtQuick.Layouts 1.3
import UM 1.1 as UM

ColumnLayout
{
    Button
    {
        text: "Back to collections"
        visible: ThingiService.isFromCollection === true && ThingiService.isQuerying === false
        Layout.leftMargin: 20
        Layout.topMargin: 10
        Layout.bottomMargin: 10
        onClicked: {
            ThingiService.getCollections()
        }
    }

    ThingsList
    {
        id: thingsList
        model: ThingiService.things
        Layout.fillWidth: true
        Layout.fillHeight: true
        Layout.topMargin: 20
    }

    RowLayout
    {
        height: 40
        Layout.fillWidth: true
        Layout.alignment: Qt.AlignBottom
        Layout.margins: 20

        Button
        {
            text: "Previous page"
            visible: ThingiService.currentPage > 1
            onClicked: {
                ThingiService.previousPage()
                Analytics.trackEvent("previous_page", "button_clicked")
            }
        }

        Button
        {
            text: "Next page"
            visible: true // TODO: hide when no more results
            onClicked: {
                ThingiService.nextPage()
                Analytics.trackEvent("next_page", "button_clicked")
            }
        }

        Label
        {
            text: "Page " + ThingiService.currentPage
            font: UM.Theme.getFont("medium")
            renderType: Text.NativeRendering
        }

        AnimatedImage
        {
            source: "images/loading.gif"
            visible: ThingiService.isQuerying
        }
    }
}
