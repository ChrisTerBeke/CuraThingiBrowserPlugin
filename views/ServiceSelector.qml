import QtQuick 2.0
import QtQuick.Controls 2.3

EnhancedComboBox
{
    id: serviceSelector
    textRole: "label"
    valueRole: "key"
    currentIndex: serviceSelector.indexOfValue(ThingiService.activeDriver)
    model: ThingiService.drivers
    onActivated: {
        ThingiService.setActiveDriver(currentValue)
        Analytics.trackEvent("driver_selected", "button_clicked")
    }
}
