// Copyright (c) 2020 Chris ter Beke.
// Thingiverse plugin is released under the terms of the LGPLv3 or higher.
import QtQuick 2.2
import QtQuick.Controls 2.0
import QtQuick.Layouts 1.3
import UM 1.1 as UM

RowLayout
{
    id: thingiSettingsItem

    property var type: ""
    property var key: ""
    property var label: ""
    property var value: ""
    property var options: []

    Label
    {
        text: thingiSettingsItem.label
        font: UM.Theme.getFont("default")
        color: UM.Theme.getColor("text")
        renderType: Text.NativeRendering
        Layout.preferredWidth: parent.width / 2 // causes both the label and input to be the same width
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
}
