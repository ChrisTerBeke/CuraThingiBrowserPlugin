import QtQuick 2.2
import QtQuick.Controls 2.0
import QtQuick.Layouts 1.3
import UM 1.1 as UM
import Cura 1.0 as Cura
import QtGraphicalEffects 1.0 // For the dropshadow

Button
{
    id: configButton
    height: parent.height
    width: parent.height // make it square

    property color backgroundColor: UM.Theme.getColor("action_button")
    property color hoverColor: UM.Theme.getColor("toolbar_button_hover")
    onClicked: {
        ThingiService.openSettings()
    }
    hoverEnabled: true

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

    DropShadow
    {
        id: shadow
        // Don't blur the shadow
        radius: 0
        anchors.fill: configBackground
        source: configBackground
        verticalOffset: 2
        visible: true
        color: UM.Theme.getColor("action_button_shadow")
        // Should always be drawn behind the background.
        z: configBackground.z - 1
    }
}
