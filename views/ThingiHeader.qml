// Copyright (c) 2020 Chris ter Beke.
// Thingiverse plugin is released under the terms of the LGPLv3 or higher.
import QtQuick 2.2
import QtQuick.Controls 2.0
import QtQuick.Layouts 1.3
import UM 1.1 as UM
import Cura 1.0 as Cura

// the main window header
Item
{
    id: header
    width: parent.width
    height: UM.Theme.getSize("toolbox_header").height
    anchors {
        top: parent.top
        left: parent.left
        right: parent.right
        margins: 5
    }

    ThingiSearchbar {
        id: searchbar
        height: parent.height
        anchors {
            top: parent.top
            bottom: parent.bottom
            left: parent.left
            right: configButton.left
            leftMargin: 10
            rightMargin: 10
        }
    }

    ConfigButton {
        id: configButton
        anchors {
            top: parent.top
            bottom: parent.bottom
            right: parent.right
        }
    }
}
