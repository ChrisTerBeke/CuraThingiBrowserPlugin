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
        font: UM.Theme.getFont("normal")
        color: UM.Theme.getColor("text")
        renderType: Text.NativeRendering
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

    ComboBox
    {
        id: inputMenu
        visible: thingiSettingsItem.type == "combobox"
        Layout.fillWidth: true
        textRole: "label"
        currentIndex: ThingiService.getDriverIndex(thingiSettingsItem.value)
        model: thingiSettingsItem.options
        onActivated: {
            ThingiService.saveSetting(thingiSettingsItem.key, model[currentIndex].key)
        }
    }

    Binding
    {
        target: thingiSettingsItem
        property: "value"
        value: thingiSettingsItem.type == "combobox" ? inputMenu.model[inputMenu.currentIndex].key : inputField.text
    }
}
