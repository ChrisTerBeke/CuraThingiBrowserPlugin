import QtQuick 2.2
import QtQuick.Controls 2.3

EnhancedComboBox
{
    id: viewSelector
    textRole: "label"
    customValueRole: "key"
    currentIndex: viewSelector.indexOfValue(ThingiService.activeView)
    sizeToContents: true
    model: ThingiService.views
    onActivated: {
        ThingiService.setActiveView(customCurrentValue)
        Analytics.trackEvent("view_selected_" + customCurrentValue, "combobox_option_selected")
    }
}
