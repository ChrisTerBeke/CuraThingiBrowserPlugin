import QtQuick 2.2
import QtQuick.Controls 2.2
import UM 1.1 as UM

TextField {
    id: textField
    font: UM.Theme.getFont("default")
    renderType: Text.NativeRendering
    selectByMouse: true
}
