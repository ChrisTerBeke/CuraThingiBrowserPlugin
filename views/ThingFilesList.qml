// Copyright (c) 2020 Chris ter Beke.
// Thingiverse plugin is released under the terms of the LGPLv3 or higher.
import QtQuick 2.7
import QtQuick.Controls 2.2
import QtQuick.Layouts 1.3

ScrollView
{
    property alias model: thingFilesList.model
    width: parent.width
    clip: true

    ListView
    {
        id: thingFilesList
        width: parent.width
        spacing: 20
        delegate: Item
        {
            width: parent.width
            height: childrenRect.height

            ThingFilesListItem
            {
                width: parent.width
                thingFile: modelData
            }
        }
    }
}
