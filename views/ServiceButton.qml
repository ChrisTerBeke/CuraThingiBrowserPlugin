// Copyright (c) 2018 Chris ter Beke.
// Thingiverse plugin is released under the terms of the LGPLv3 or higher.
import QtQuick 2.2
import QtQuick.Controls 2.2
import QtQuick.Layouts 1.3
import UM 1.1 as UM
import Cura 1.0 as Cura

Label {
    property url backgroundImageSource: ""
    property color backgroundColor: UM.Theme.getColor("action_button")
    property color hoverColor: UM.Theme.getColor("toolbar_button_hover")

    signal clicked()

    id: buttonLabel
    color: UM.Theme.getColor("text")
    font: UM.Theme.getFont("medium")
    width: parent.width
    Layout.fillWidth: true
    Layout.alignment: Qt.AlignLeft | Qt.AlignCenter
    padding: UM.Theme.getSize("default_margin").height

    background: Item {
        id: buttonBackgroundItem
        anchors.fill: buttonLabel

        Rectangle {
            id: buttonBackground
            height: parent.height
            width: parent.width
            radius: 0
            color: backgroundColor
            anchors.fill: parent
        }

        Image {
            id: thingiverseLogo
            anchors.fill: parent
            anchors{ leftMargin: UM.Theme.getSize("default_margin").width; rightMargin: UM.Theme.getSize("default_margin").width }
            fillMode: Image.PreserveAspectFit
            source: buttonLabel.backgroundImageSource
        }

        Component.onCompleted: color = UM.Theme.getColor("main_background")
    }

    MouseArea
    {
        id: mouseArea
        anchors.fill: parent
        onClicked: buttonLabel.clicked()
        onEntered: buttonBackground.color = hoverColor
        onExited: buttonBackground.color = backgroundColor
        hoverEnabled: true
        cursorShape: Qt.PointingHandCursor
    }
}
