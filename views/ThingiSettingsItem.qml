// Copyright (c) 2020.
// Thingiverse plugin is released under the terms of the LGPLv3 or higher.
import QtQuick 2.2
import QtQuick.Controls 2.0
import QtQuick.Layouts 1.3
import UM 1.1 as UM

RowLayout
{
    id: thingiSettingsItem
    width: parent.width

    property var type: ""
    property var key: ""
    property var label: ""
    property var value: ""
    property var options: []
    property var driver: ""
    property var description: ""

    Label
    {
        id: label
        text: thingiSettingsItem.label
        font: UM.Theme.getFont("default")
        color: UM.Theme.getColor("text")
        renderType: Text.NativeRendering
        Layout.preferredWidth: parent.width / 2 // causes both the label and input to be the same width

        ToolTip {
            id: labelToolTip
            visible: labelHoverArea.containsMouse
            width: thingiSettingsItem.width * 0.75
            delay: 500
            contentItem: Text {
                text: thingiSettingsItem.description
                wrapMode: Text.WordWrap
            }
        }

        MouseArea {
            id: labelHoverArea
            anchors.fill: parent
            hoverEnabled: true
        }
    }

    TextField
    {
        id: inputField
        text: thingiSettingsItem.value
        visible: thingiSettingsItem.type == "text"
        Layout.fillWidth: true
        selectByMouse: true
        onEditingFinished: {
            ThingiService.saveSetting(thingiSettingsItem.key, thingiSettingsItem.value)
        }
    }

    EnhancedComboBox
    {
        id: inputMenu
        visible: thingiSettingsItem.type == "combobox"
        Layout.fillWidth: true
        textRole: "label"
        customValueRole: "key"
        currentIndex: indexOfValue(thingiSettingsItem.value)
        model: thingiSettingsItem.options
        onActivated: {
            ThingiService.saveSetting(thingiSettingsItem.key, customCurrentValue)
        }
    }

    Button
    {
        id: callToActionButtonAuthenticate
        visible: thingiSettingsItem.type == "cta_button" && thingiSettingsItem.value == ""
        Layout.fillWidth: true
        text: "Sign In"
        onClicked: {
            ThingiService.authenticateDriver(thingiSettingsItem.driver)
        }
    }

    Button
    {
        id: callToActionButtonRevoke
        visible: thingiSettingsItem.type == "cta_button" && thingiSettingsItem.value !== ""
        Layout.fillWidth: true
        text: "Sign Out"
        onClicked: {
            ThingiService.clearAuthenticationForDriver(thingiSettingsItem.driver)
        }
    }

    Binding
    {
        target: thingiSettingsItem
        property: "value"
        when: thingiSettingsItem.type == "text"
        value: inputField.text
    }

    Binding
    {
        target: thingiSettingsItem
        property: "value"
        when: thingiSettingsItem.type == "combobox"
        value: inputMenu.currentIndex < 0 ? "" : inputMenu.model[inputMenu.currentIndex][inputMenu.customValueRole]
    }

    Binding
    {
        target: callToActionButtonRevoke
        property: "visible"
        when: thingiSettingsItem.type == "cta_button"
        value: thingiSettingsItem.value !== ""
    }

    Binding
    {
        target: callToActionButtonAuthenticate
        property: "visible"
        when: thingiSettingsItem.type == "cta_button"
        value: thingiSettingsItem.value == ""
    }
}
