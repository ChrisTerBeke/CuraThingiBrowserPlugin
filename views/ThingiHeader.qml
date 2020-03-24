import QtQuick 2.2
import QtQuick.Controls 2.3
import QtQuick.Layouts 1.3

// the main window header
RowLayout
{
    width: parent.width
    height: 40
    spacing: 0

    ServiceSelector
    {
        id: serviceSelector
    }

    ViewSelector
    {
        id: viewSelector
    }

    ThingiSearchbar
    {
        id: searchbar
        Layout.fillWidth: true
    }

    Button
    {
        id: configButton
        text: "Settings"
        onClicked: {
            ThingiService.openSettings()
            Analytics.trackEvent("config_button", "clicked")
        }
    }
}
