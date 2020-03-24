// Copyright (c) 2020 Chris ter Beke.
// Thingiverse plugin is released under the terms of the LGPLv3 or higher.
import QtQuick 2.2
import QtQuick.Controls 2.2
import QtQuick.Layouts 1.3
import UM 1.1 as UM

ColumnLayout
{
    id: detailsPage

    // the active thing
    property var thing

    // the files for the active thing
    property var thingFiles

    // button to navigate back to the search results page
    Button
    {
        text: "Back to results"
        Layout.leftMargin: 20
        Layout.topMargin: 10
        Layout.bottomMargin: 10
        onClicked: {
            ThingiService.hideThingDetails()
            Analytics.trackEvent("back_to_results", "button_clicked")
        }
    }

    Label
    {
        id: thingTitle
        text: thing ? thing.name : ""
        font: UM.Theme.getFont("large")
        color: UM.Theme.getColor("text")
        renderType: Text.NativeRendering
        Layout.leftMargin: 20
        Layout.bottomMargin: 10
    }

    // link to web page
    Link
    {
        text: thing ? thing.url : ""
        url: thing ? thing.url : ""
        Layout.leftMargin: 20
        Layout.bottomMargin: 20
    }

    ScrollView
    {
        id: scroller
        width: detailsPage.width
        clip: true
        Layout.fillHeight: true
        Layout.bottomMargin: 20

        Column
        {
            Label
            {
                id: thingDescription
                text: thing ? thing.description : ""
                font: UM.Theme.getFont("medium")
                color: UM.Theme.getColor("text")
                renderType: Text.NativeRendering
                wrapMode: Label.WordWrap
                width: detailsPage.width
                leftPadding: 20
                bottomPadding: 20
            }

            ThingFilesList
            {
                id: thingFilesList
                model: thingFiles
            }

            Label
            {
                id: thingFilesListEmpty
                text: "There are no files in this Thing that can be imported in Cura."
                visible: thingFiles.length === 0
                font: UM.Theme.getFont("medium")
                color: UM.Theme.getColor("text_inactive")
                renderType: Text.NativeRendering
                wrapMode: Label.WordWrap
                width: detailsPage.width
                leftPadding: 20
            }
        }
    }
}
