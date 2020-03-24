// Copyright (c) 2020 Chris ter Beke.
// Thingiverse plugin is released under the terms of the LGPLv3 or higher.
import QtQuick 2.2
import QtQuick.Controls 2.0
import QtQuick.Layouts 1.3
import UM 1.1 as UM

RowLayout
{
    id: thingiSettingsItem

    property var key: ""
    property var label: ""
    property var value: ""

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
        Layout.fillWidth: true
        selectByMouse: true
        onEditingFinished: {
            ThingiService.saveSetting(thingiSettingsItem.key, thingiSettingsItem.value)
        }
    }

    Binding
    {
        target: thingiSettingsItem
        property: "value"
        value: inputField.text
    }
}
