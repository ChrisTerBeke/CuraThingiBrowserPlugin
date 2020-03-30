import QtQuick 2.2
import QtQuick.Controls 2.0
import QtQuick.Layouts 1.3

ComboBox
{
    id: comboBox

    property string currentValue
    property string valueRole: "value"

    function indexOfValue(value) {
        if (model !== undefined) {
            for(var idx in model) {
                if (model[idx][valueRole] === value) {
                    return idx
                }
            }
        }
        return -1
    }

    Binding {
        target: comboBox
        property: "currentValue"
        value: currentIndex < 0 ? '' : model[currentIndex][valueRole]
    }
}
