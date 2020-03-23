import QtQuick 2.0
import QtQuick.Controls 2.0
import QtQuick.Layouts 1.3
import UM 1.1 as UM
import Cura 1.0 as Cura

Item {
    id: searchbar

    RowLayout {
        anchors.fill: parent
        spacing: 0

        ServiceSelector {
            id: serviceSelector
            anchors { top: parent.top; bottom: parent.bottom; margins: searchbarBackground.border.width }
            Layout.margins: searchbarBackground.border.width
            headerCornerSide: Cura.RoundedRectangle.Direction.Left
        }

        // Separator line
        Rectangle {
            height: parent.height - 2 // for some reason the parent height results in a too tall separator
            width: UM.Theme.getSize("default_lining").width
            color: UM.Theme.getColor("lining")
            Layout.rightMargin: UM.Theme.getSize("default_margin").width
        }

        TextField {
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

        Cura.PrimaryButton {
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
        Rectangle {
            height: parent.height - 2 // for some reason the parent height results in a too tall separator
            width: UM.Theme.getSize("default_lining").width
            color: UM.Theme.getColor("lining")
        }

        ViewSelector {
            id: viewSelector
            headerRadius: 5
            headerCornerSide: 4
            enableHeaderShadow: false
            anchors { top: parent.top; bottom: parent.bottom; margins: searchbarBackground.border.width }
            Layout.margins: searchbarBackground.border.width
        }
    }

    Rectangle {
        id: searchbarBackground
        height: parent.height
        width: parent.width
        color: UM.Theme.getColor("main_background")
        border.color: UM.Theme.getColor("lining")
        radius: UM.Theme.getSize("default_radius").width
        z: parent.z - 1
    }
}