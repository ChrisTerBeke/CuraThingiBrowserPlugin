// Copyright (c) 2018 Chris ter Beke.
// Thingiverse plugin is released under the terms of the LGPLv3 or higher.
import QtQuick 2.2
import QtQuick.Controls 2.0
import QtQuick.Dialogs 1.1
import QtQuick.Layouts 1.3
import QtQuick.Window 2.2
import UM 1.1 as UM
import Cura 1.0 as Cura

// the popup window
Window
{
    id: thingisettings

    // window configuration
    color: UM.Theme.getColor("main_background")
    minimumWidth: Math.round(UM.Theme.getSize("license_window_minimum").width)
    width: minimumWidth

    title: "Thingiverse Settings"

    // area to provide un-focus option for search field
    MouseArea
    {
        anchors.fill: parent
        focus: true
        onClicked: {
            focus = true
        }
    }

    ColumnLayout
    {
        anchors.fill: parent
        anchors.margins: 20

        GridLayout
        {
            columns: 2
            Layout.minimumWidth: parent.width
            Layout.minimumHeight: parent.height - UM.Theme.getSize("toolbox_header").height
            Layout.fillHeight: true

            Label
            {
                id: lblThingiUserField
                text: "Account Name"
                Layout.alignment: Qt.AlignRight | Qt.AlignTop
                font: UM.Theme.getFont("large")
                color: UM.Theme.getColor("text")
                renderType: Text.NativeRendering
                Layout.rightMargin: 10
            }

            TextField
            {
                id: thingiUserField
                placeholderText: "Your Account Name..."
                text: ThingiService.userName
                Layout.alignment: Qt.AlignLeft | Qt.AlignTop
                Layout.fillWidth: true
                onAccepted: {
                    ThingiService.saveSetting("user_name", thingiUserField.text)
                    thingisettings.close()
                }
                selectByMouse: true
            }
        }

        RowLayout
        {
            Item
            {
                Layout.fillWidth: true
            }

            Cura.PrimaryButton
            {
                id: btnSave
                text: "Save"
                onClicked: {
                    ThingiService.saveSetting("user_name", thingiUserField.text)
                    thingisettings.close()
                }
                Layout.alignment: Qt.AlignRight
            }
        }
    }
}
