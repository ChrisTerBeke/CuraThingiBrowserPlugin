import QtQuick 2.2
import QtQuick.Controls 2.2
import UM 1.1 as UM

Button {
    id: button

    contentItem: Label {
        text: button.text
        font: UM.Theme.getFont("default")
        renderType: Text.NativeRendering
        anchors.fill: parent
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
        elide: Text.ElideRight
    }
}
