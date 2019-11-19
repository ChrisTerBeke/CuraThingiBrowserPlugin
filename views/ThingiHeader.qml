// Copyright (c) 2018 Chris ter Beke.
// Thingiverse plugin is released under the terms of the LGPLv3 or higher.
import QtQuick 2.2
import QtQuick.Controls 2.0
import QtQuick.Layouts 1.3
import UM 1.1 as UM
import Cura 1.0 as Cura
import QtGraphicalEffects 1.0 // For the dropshadow

// the main window header
Item
{
    id: header
    width: parent.width
    height: UM.Theme.getSize("toolbox_header").height
    anchors.top: parent.top
    anchors.left: parent.left
    anchors.right: parent.right
    anchors.margins: 20
    Layout.bottomMargin: 20

    ThingiSearchbar
    {
        id: searchbar
        height: parent.height
        anchors.top: parent.top
        anchors.bottom: parent.bottom
        anchors.left: parent.left
        anchors.right: configButton.left
        anchors.rightMargin: 10
    }

    ConfigButton
    {
        id: configButton
        anchors.top: parent.top
        anchors.bottom: parent.bottom
        anchors.right: parent.right
    }
}
