import QtQuick 2.7
import QtQuick.Controls 2.0
import QtQuick.Layouts 1.3

ComboBox
{
    id: comboBox

    property string customCurrentValue
    property string customValueRole: "value"
    property int implicitIndicatorWidth: 20
    property bool sizeToContents: false
    property int modelWidth

    Layout.preferredWidth: (sizeToContents) ? modelWidth : implicitWidth

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

    TextMetrics 
    {
        id: textMetrics
    }

    onModelChanged: {
        var _maxWidth = 0
        for(var idx in model){
            textMetrics.text = model[idx][textRole]
            _maxWidth = Math.max(textMetrics.width, _maxWidth)
        }
        modelWidth = _maxWidth + implicitIndicatorWidth*2 + leftPadding + rightPadding + contentItem.leftPadding + contentItem.rightPadding
        console.log("Model Width set to: "+modelWidth)
    }

    Binding {
        target: comboBox
        property: "customCurrentValue"
        value: currentIndex < 0 ? "" : model[currentIndex][customValueRole]
    }
}
