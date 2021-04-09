import QtQuick 2.7
import QtQuick.Controls 2.0
import UM 1.1 as UM

ComboBox {
    id: comboBox

    property string customCurrentValue
    property string customValueRole: "value"

    contentItem: Label {
        text: comboBox.displayText
        font: UM.Theme.getFont("default")
        renderType: Text.NativeRendering
        anchors.fill: parent
        leftPadding: 10
        verticalAlignment: Text.AlignVCenter
        elide: Text.ElideRight
    }

    delegate: ItemDelegate {
        highlighted: comboBox.highlightedIndex === index
        width: comboBox.width
        contentItem: Label {
            text: comboBox.model[index][comboBox.textRole]
            font: UM.Theme.getFont("default")
            renderType: Text.NativeRendering
            anchors.fill: parent
            leftPadding: 10
            verticalAlignment: Text.AlignVCenter
            elide: Text.ElideRight
        }
    }

    Binding {
        target: comboBox
        property: "customCurrentValue"
        value: currentIndex < 0 ? "" : model[currentIndex][customValueRole]
    }

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
}
