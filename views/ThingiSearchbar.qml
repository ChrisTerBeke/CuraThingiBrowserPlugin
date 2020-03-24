import QtQuick 2.0
import QtQuick.Controls 2.0
import QtQuick.Layouts 1.3
import UM 1.1 as UM

RowLayout
{
    TextField
    {
        id: thingSearchField
        placeholderText: "Search for things..."
        Layout.fillWidth: true
        selectByMouse: true
        onAccepted: {
            ThingiService.search(thingSearchField.text)
            Analytics.trackEvent("search_field", "enter_pressed")
        }
    }

    Button
    {
        text: "Search"
        Layout.alignment: Qt.AlignLeft
        onClicked: {
            ThingiService.search(thingSearchField.text)
            Analytics.trackEvent("search_field", "button_clicked")
        }
    }
}
