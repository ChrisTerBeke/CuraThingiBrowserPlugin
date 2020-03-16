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

    // hide the whole page if no thing is actually set
    visible: thing != undefined

    // button to navigate back to the search results page
    Cura.SecondaryButton
    {
        text: catalog.i18nc("@button", "Back to results")
        onClicked: {
            ThingiService.hideThingDetails()
            Analytics.trackEvent("back_to_results", "button_clicked")
        }
        Layout.leftMargin: 20
        Layout.topMargin: 10
        Layout.bottomMargin: 10
    }

    Label
    {
        id: thingTitle
        text: thing.NAME
        font: UM.Theme.getFont("large")
        color: UM.Theme.getColor("text")
        renderType: Text.NativeRendering
        Layout.leftMargin: 20
        Layout.bottomMargin: 10
    }

    // link to web page
    Link
    {
        text: thing.URL
        url: thing.URL
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
                text: thing.DESCRIPTION
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
