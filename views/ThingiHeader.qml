// Copyright (c) 2018 Chris ter Beke.
// Thingiverse plugin is released under the terms of the LGPLv3 or higher.
import QtQuick 2.2
import QtQuick.Controls 2.0
import QtQuick.Dialogs 1.1
import QtQuick.Layouts 1.3
import QtQuick.Window 2.2
import UM 1.1 as UM
import Cura 1.0 as Cura

// the main window header
Rectangle
{
    id: header

    width: parent.width
    Layout.fillWidth: true
    height: UM.Theme.getSize("toolbox_header").height
    color: "#f5f5f5"

    RowLayout
    {
        height: parent.height
        width: parent.width

        Image
        {
            sourceSize.width: 100
            source: "thingiverse-logo-2015.png"
            Layout.leftMargin: 20
            Layout.rightMargin: 20
        }

        TextField
        {
            id: thingSearchField
            placeholderText: "Search for things..."
            Layout.alignment: Qt.AlignCenter
            Layout.preferredWidth: parent.width / 2
            onAccepted: ThingiService.search(thingSearchField.text)
            selectByMouse: true
        }

        Cura.PrimaryButton
        {
            text: "Search"
            onClicked: ThingiService.search(thingSearchField.text)
            Layout.alignment: Qt.AlignCenter
        }

        Item
        {
            Layout.fillWidth: true
        }
    }
}
