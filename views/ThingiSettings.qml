// Copyright (c) 2018 Chris ter Beke.
// Thingiverse plugin is released under the terms of the LGPLv3 or higher.
import QtQuick 2.2
import QtQuick.Controls 2.0
import QtQuick.Dialogs 1.1
import QtQuick.Layouts 1.3
import QtQuick.Window 2.2
import UM 1.1 as UM

// the popup window
Window
{
    id: thingiSettingsWindow

    // window configuration
    color: UM.Theme.getColor("viewport_background")
    minimumWidth: 500
    minimumHeight: 300
    width: minimumWidth
    height: minimumHeight
    title: "ThingiBrower - Settings"

    // area to provide un-focus option for input fields
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

        Repeater
        {
            model: ThingiService.getSettings
            ThingiSettingsItem
            {
                type: modelData.type
                key: modelData.key
                label: modelData.label
                value: modelData.value
                description: modelData.description
                options: modelData.options
                driver: modelData.driver
            }
        }

        RowLayout
        {
            Item
            {
                Layout.fillWidth: true
            }

            Button
            {
                id: btnSave
                text: "Close"
                onClicked: {
                    thingiSettingsWindow.close()
                }
            }
        }
    }
}
