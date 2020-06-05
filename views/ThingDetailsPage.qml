// Copyright (c) 2020.
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

    // name
    Label
    {
        id: thingTitle
        text: thing && thing.name ? thing.name : ""
        font: UM.Theme.getFont("large")
        color: UM.Theme.getColor("text")
        renderType: Text.NativeRendering
        wrapMode: Label.WordWrap
        Layout.fillWidth: true
        Layout.leftMargin: 20
        Layout.bottomMargin: 10
        Layout.rightMargin: 20
    }

    // link to web page
    Link
    {
        text: thing && thing.url ? thing.url : ""
        url: thing && thing.url ? thing.url : ""
        elide: Text.ElideRight
        Layout.leftMargin: 20
        Layout.bottomMargin: 20
    }

    // description
    Label
    {
        id: thingDescription
        text: thing && thing.description ? thing.description : ""
        font: UM.Theme.getFont("medium")
        color: UM.Theme.getColor("text")
        renderType: Text.NativeRendering
        wrapMode: Label.WordWrap
        Layout.fillWidth: true
        Layout.fillHeight: true
        Layout.leftMargin: 20
        Layout.bottomMargin: 20
        Layout.rightMargin: 20
        clip: true
        elide: Text.ElideRight
    }

    ThingFilesList
    {
        id: thingFilesList
        model: thingFiles
        visible: thingFiles.length > 0
        Layout.fillWidth: true
        Layout.fillHeight: true
        Layout.leftMargin: 20
        Layout.rightMargin: 20
        Layout.bottomMargin: 20
    }

    Label
    {
        id: thingFilesListEmpty
        text: "There are no files in this Thing that can be imported in Cura."
        visible: !thingFilesList.visible
        font: UM.Theme.getFont("medium")
        color: UM.Theme.getColor("text_inactive")
        renderType: Text.NativeRendering
        wrapMode: Label.WordWrap
        Layout.fillWidth: true
        Layout.fillHeight: true
        Layout.leftMargin: 20
    }
}
