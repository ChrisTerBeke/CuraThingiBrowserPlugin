import QtQuick 2.0
import QtQuick.Controls 2.3

EnhancedComboBox {
    id: serviceSelector

    textRole: "label"
    customValueRole: "key"
    currentIndex: serviceSelector.indexOfValue(ThingiService.activeDriver)
    model: ThingiService.drivers

    onActivated: {
        ThingiService.setActiveDriver(customCurrentValue)
        Analytics.trackEvent("driver_selected_" + customCurrentValue, "combobox_option_selected")
    }
}
