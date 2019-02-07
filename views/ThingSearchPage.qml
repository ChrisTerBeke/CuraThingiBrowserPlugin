// Copyright (c) 2018 Chris ter Beke.
// Thingiverse plugin is released under the terms of the LGPLv3 or higher.
import QtQuick 2.2
import QtQuick.Controls 2.0
import QtQuick.Dialogs 1.1
import QtQuick.Layouts 1.3
import QtQuick.Window 2.2
import UM 1.1 as UM


ColumnLayout
{
    anchors.fill: parent

    TextField
    {
        id: thingSearchField
        placeholderText: "Search for things..."
        onEditingFinished: ThingiService.search(thingSearchField.text)
    }

    ThingsList
    {
        id: thingsList
        model: ThingiService.things
        Layout.fillWidth: true
        Layout.fillHeight: true
    }
}
