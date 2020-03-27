import QtQuick 2.0
import QtQuick.Controls 2.3

ComboBox
{
    textRole: "label"
    model: ThingiService.drivers
    currentIndex: ThingiService.getDriverIndex(ThingiService.activeDriver)
    onActivated: {
        ThingiService.setActiveDriver(model[currentIndex].key)
        Analytics.trackEvent("driver_selected", "button_clicked")
    }
}
