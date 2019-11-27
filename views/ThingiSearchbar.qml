import QtQuick 2.0
import QtQuick.Controls 2.0
import QtQuick.Layouts 1.3
import UM 1.1 as UM
import Cura 1.0 as Cura

Item
{
    id: searchbar

    RowLayout
    {
        height: parent.height
        width: parent.width
        spacing: 0

        Image
        {
            sourceSize.width: 100
            source: "thingiverse-logo-2015.png"
            Layout.leftMargin: UM.Theme.getSize("default_margin").width
            Layout.rightMargin: UM.Theme.getSize("default_margin").width

            // make the header image clickable
            MouseArea
            {
                anchors.fill: parent
                onClicked: {
                    viewSelector.labelText = "Search"
                    ThingiService.search("ultimaker")
                    Analytics.trackEvent("header_image", "clicked")
                }
                hoverEnabled: true
                cursorShape: Qt.PointingHandCursor
            }
        }

        TextField
        {
            id: thingSearchField
            placeholderText: "Search for things..."
            Layout.alignment: Qt.AlignCenter
            Layout.fillWidth: true
            Layout.rightMargin: UM.Theme.getSize("default_margin").width
            onAccepted: {
                viewSelector.labelText = "Search"
                ThingiService.search(thingSearchField.text)
                Analytics.trackEvent("search_field", "enter_pressed")
            }
            selectByMouse: true
        }

        Cura.PrimaryButton
        {
            text: "Search"
            onClicked: {
                viewSelector.labelText = "Search"
                ThingiService.search(thingSearchField.text)
                Analytics.trackEvent("search_field", "button_clicked")
            }
            Layout.alignment: Qt.AlignCenter
            Layout.rightMargin: UM.Theme.getSize("default_margin").width
        }

        // Separator line
        Rectangle
        {
            id: separatorLine
            height: parent.height - 2 // for some reason the parent height results in a too tall separator
            width: UM.Theme.getSize("default_lining").width
            color: UM.Theme.getColor("lining")
        }

        ViewSelector
        {
            id: viewSelector
            headerRadius: 5
            headerCornerSide: 4
            enableHeaderShadow: false
            anchors.top: parent.top
            anchors.bottom: parent.bottom
            anchors.margins: searchbarBackground.border.width
            Layout.margins: searchbarBackground.border.width
        }
    }

    Rectangle
    {
        id: searchbarBackground
        height: parent.height
        width: parent.width
        color: UM.Theme.getColor("main_background")
        border.color: UM.Theme.getColor("lining")
        radius: UM.Theme.getSize("default_radius").width
        z: parent.z - 1
    }
}
