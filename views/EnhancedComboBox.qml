import QtQuick 2.2
import QtQuick.Controls 2.0
import QtQuick.Layouts 1.3

ComboBox
{
    id: comboBox

    property string customCurrentValue
    property string customValueRole: "value"

    function indexOfValue(value) {
        if (model == undefined) {
            return -1
        }
        for (var idx in model) {
            if (model[idx][customValueRole] === value) {
                return idx
            }
        }
    }

    Binding {
        target: comboBox
        property: "customCurrentValue"
        value: currentIndex < 0 ? "" : model[currentIndex][customValueRole]
    }
}
