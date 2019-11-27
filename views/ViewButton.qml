// Copyright (c) 2018 Chris ter Beke.
// Thingiverse plugin is released under the terms of the LGPLv3 or higher.
import QtQuick 2.2
import QtQuick.Controls 2.2
import QtQuick.Layouts 1.3
import UM 1.1 as UM
import Cura 1.0 as Cura

Label
{
    id: buttonLabel

    property color backgroundColor: UM.Theme.getColor("action_button")
    property color hoverColor: UM.Theme.getColor("toolbar_button_hover")
    signal clicked()
    color: UM.Theme.getColor("text")
    background: Rectangle
    {
        id: background
        height: parent.height
        width: parent.width
        color: backgroundColor
        radius: 0
        anchors.fill: parent
    }
    font: UM.Theme.getFont("medium")
    width: parent.width
    Layout.fillWidth: true
    Layout.alignment: Qt.AlignLeft | Qt.AlignCenter
    padding: UM.Theme.getSize("default_margin").height

    MouseArea
    {
        id: mouseArea
        anchors.fill: parent
        onClicked: buttonLabel.clicked()
        onEntered: background.color = hoverColor
        onExited: background.color = backgroundColor
        hoverEnabled: true
        cursorShape: Qt.PointingHandCursor
    }
}
