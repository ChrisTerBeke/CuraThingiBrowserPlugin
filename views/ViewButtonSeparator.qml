import QtQuick 2.2
import QtQuick.Layouts 1.3
import UM 1.1 as UM

// Separator line
Rectangle
{
    height: UM.Theme.getSize("default_lining").height
    width: parent.width
    Layout.fillWidth: true
    color: UM.Theme.getColor("lining")
}
