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
    minimumWidth: Math.round(UM.Theme.getSize("modal_window_minimum").width)
    minimumHeight: Math.round(UM.Theme.getSize("modal_window_minimum").height)
    width: minimumWidth
    height: minimumHeight

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
        width: parent.width

        RowLayout
        {
            Layout.topMargin: 20
            Layout.leftMargin: 20
            Layout.rightMargin: 20

            Label
            {
                id: lblThingiUserField
                text: "Account Name"
                Layout.alignment: Qt.AlignLeft
                font: UM.Theme.getFont("large")
                color: UM.Theme.getColor("text")
                renderType: Text.NativeRendering
                Layout.rightMargin: 10
            }

            TextField
            {
                id: thingiUserField
                placeholderText: "Your Account Name..."
                text: UM.Preferences.getValue("ThingiBrowser/user_name")
                Layout.alignment: Qt.AlignLeft
                Layout.fillWidth: true
                onAccepted: {
                    UM.Preferences.saveValue("ThingiBrowser/user_name", thingiUserField.text)
                }
                selectByMouse: true
            }
        }

        Cura.PrimaryButton
        {
            text: "Save"
            onClicked: {
                UM.Preferences.saveValue("ThingiBrowser/user_name", thingiUserField.text)
                thingisettings.close()
            }
            Layout.rightMargin: 20
            Layout.alignment: Qt.AlignRight
        }
    }
}
