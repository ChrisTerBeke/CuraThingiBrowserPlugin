// Copyright (c) 2020.
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
        visible: ThingiService.isFromCollection === true
        Layout.leftMargin: 20
        Layout.topMargin: 10
        onClicked: {
            ThingiService.getCollections()
            Analytics.trackEvent("back_to_collections", "button_clicked")
        }
    }

    Label
    {
        text: "No results. Please try another category or search term or configure your account in the settings window."
        visible: ThingiService.things.length == 0 && ThingiService.isQuerying == false
        font: UM.Theme.getFont("default")
        renderType: Text.NativeRendering
        horizontalAlignment: Text.AlignHCenter
        Layout.fillWidth: true
        Layout.fillHeight: true
        Layout.topMargin: 20
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
            visible: ThingiService.currentPage > 1 && ThingiService.things.length > 0
            onClicked: {
                ThingiService.previousPage()
                Analytics.trackEvent("previous_page", "button_clicked")
            }
        }

        // FIXME: hide when reaching last page of results (can be done now that we have 'total' in Thingiverse api)
        Button
        {
            text: "Next page"
            visible: ThingiService.things.length > 0
            onClicked: {
                ThingiService.nextPage()
                Analytics.trackEvent("next_page", "button_clicked")
            }
        }

        Label
        {
            text: "Page " + ThingiService.currentPage
            visible: ThingiService.things.length > 0
            font: UM.Theme.getFont("medium")
            color: UM.Theme.getColor("text")
            renderType: Text.NativeRendering
        }

        AnimatedImage
        {
            source: "images/loading.gif"
            visible: ThingiService.isQuerying
        }
    }
}
