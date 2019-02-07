// Copyright (c) 2018 Ultimaker B.V.
// Cura is released under the terms of the LGPLv3 or higher.
import QtQuick 2.7
import QtQuick.Controls 2.1
import QtQuick.Layouts 1.3
import QtQuick.Dialogs 1.1

import UM 1.1 as UM
import Cura 1.0 as Cura

Item
{
    id: thingTile
    width: parent.width
    height: dataRow.height
    property var thing: null

    RowLayout
    {
        id: dataRow
        spacing: UM.Theme.getSize("wide_margin").width
        width: parent.width
        height: 100 * screenScaleFactor

        Label
        {
            text: thing.name
            color: UM.Theme.getColor("text")
            elide: Text.ElideRight
            Layout.minimumWidth: 100 * screenScaleFactor
            Layout.maximumWidth: 500 * screenScaleFactor
            Layout.fillWidth: true
            font: UM.Theme.getFont("default")
            renderType: Text.NativeRendering
        }

        Image
        {
            source: thing.thumbnail
        }

        Cura.PrimaryButton
        {
            text: catalog.i18nc("@button", "Details")
            onClicked: ThingiService.showThingDetails(thing.id)
        }
    }
}
