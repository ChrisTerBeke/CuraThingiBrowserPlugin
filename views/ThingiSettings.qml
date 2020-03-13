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
Window {
    id: thingiSettingsWindow

    // window configuration
    title: "Thingiverse Settings"
    color: UM.Theme.getColor("viewport_background")
    width: 300

    // area to provide un-focus option for input fields
    MouseArea {
        anchors.fill: parent
        focus: true
        onClicked: {
            focus = true
        }
    }

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 20

        ThingiSettingsItem {
            id: thingiverseUserNameSettingsItem
            label: "Thingiverse Account Name"
            value: ThingiService.thingiverseUserName
        }

        ThingiSettingsItem {
            id: myMiniFactoryUserNameSettingsItem
            label: "MyMiniFactory Account Name"
            value: ThingiService.myMiniFactoryUserName
        }

        RowLayout {
            Item {
                Layout.fillWidth: true
            }

            Cura.PrimaryButton {
                id: btnSave
                text: "Save"
                onClicked: {
                    ThingiService.saveSetting("user_name", thingiverseUserNameSettingsItem.value)
                    ThingiService.saveSetting("myminifactory_user_name", myMiniFactoryUserNameSettingsItem.value)
                    thingiSettingsWindow.close()
                }
            }
        }
    }
}
