import QtQuick 2.0
import QtQuick.Controls 2.0
import QtQuick.Layouts 1.3
import UM 1.1 as UM
import Cura 1.0 as Cura

Rectangle
{
    color: UM.Theme.getColor("main_background")
    border.color: UM.Theme.getColor("lining")
    radius: UM.Theme.getSize("default_radius").width

    RowLayout
    {
        TextField
        {
            id: thingSearchField
            placeholderText: "Search for things..."
            Layout.fillWidth: true
            selectByMouse: true
            onAccepted: {
                viewSelector.labelText = "Search"
                ThingiService.search(thingSearchField.text)
                Analytics.trackEvent("search_field", "enter_pressed")
            }
        }

        Cura.PrimaryButton
        {
            text: "Search"
            Layout.alignment: Qt.AlignCenter
            Layout.rightMargin: UM.Theme.getSize("default_margin").width
            onClicked: {
                viewSelector.labelText = "Search"
                ThingiService.search(thingSearchField.text)
                Analytics.trackEvent("search_field", "button_clicked")
            }
        }
    }
}
