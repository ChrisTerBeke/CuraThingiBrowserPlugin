// Copyright (c) 2018 Chris ter Beke.
// Thingiverse plugin is released under the terms of the LGPLv3 or higher.
import QtQuick 2.7
import QtQuick.Controls 2.2
import QtQuick.Layouts 1.3

import UM 1.1 as UM

ScrollView
{
    property alias model: thingsList.model
    width: parent.width
    clip: true

    ListView
    {
        id: thingsList
        width: parent.width
        delegate: Item
        {
            width: parent.width
            height: childrenRect.height

            ThingTile
            {
                width: parent.width
                thing: modelData
            }
        }
    }
}
