import QtQuick 2.0
import QtQuick.Controls 2.3

ComboBox
{
    textRole: "text"
    model: ListModel {
        id: servicesListModel
        ListElement {
            text: "ThingiVerse"
            image: "images/thingiverse-logo-2015.png"
            value: "thingiverse"
        }
        ListElement {
            text: "MyMiniFactory"
            image: "images/my-mini-factory-logo-dropshadow-sm.png"
            value: "myminifactory"
        }
    }
    onActivated: {
        ThingiService.setActiveDriver(servicesListModel.get(currentIndex).value)
        Analytics.trackEvent("driver_selected", "button_clicked")
    }
}
