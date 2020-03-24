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
    height: 40
    anchors.margins: 5

    RowLayout
    {
        anchors.fill: parent
        spacing: 0

        ServiceSelector
        {
            id: serviceSelector
        }

//        ThingiSearchbar
//        {
//            id: searchbar
//            Layout.fillWidth: true
//        }
//
//        ViewSelector
//        {
//            id: viewSelector
//        }
//
//        ConfigButton
//        {
//            id: configButton
//        }
    }
}
