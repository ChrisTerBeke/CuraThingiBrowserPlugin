import QtQuick 2.2
import QtQuick.Controls 2.0
import QtQuick.Layouts 1.3
import UM 1.1 as UM
import Cura 1.0 as Cura

Button
{
    id: showDialogButton
    height: parent.height
    width: parent.height // make it square
    hoverEnabled: true

    property color backgroundColor: UM.Theme.getColor("action_button")
    property color hoverColor: UM.Theme.getColor("toolbar_button_hover")

    onClicked: {
        ThingiExtension.showMainWindow()
    }

    contentItem: Item
    {
        anchors.fill: parent
        UM.RecolorImage
        {
            id: buttonIcon
            anchors.centerIn: parent
            source: UM.Theme.getIcon("settings")
            width: UM.Theme.getSize("button_icon").width - UM.Theme.getSize("default_margin").width
            height: UM.Theme.getSize("button_icon").height - UM.Theme.getSize("default_margin").height
            color: UM.Theme.getColor("icon")
            sourceSize.height: height
        }
    }

    background: Rectangle
    {
        id: configBackground
        height: UM.Theme.getSize("toolbox_header").height
        width: UM.Theme.getSize("toolbox_header").height
        radius: UM.Theme.getSize("default_radius").width
        border.color: UM.Theme.getColor("lining")
        color: configButton.hovered ? hoverColor : backgroundColor
    }
}
