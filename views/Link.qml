// Copyright (c) 2020.
// Thingiverse plugin is released under the terms of the LGPLv3 or higher.
import QtQuick 2.2
import QtQuick.Controls 2.2
import QtQuick.Layouts 1.3
import UM 1.1 as UM

Label
{
    id: link
    property var url: ""

    color: UM.Theme.getColor("text_link")
    font: UM.Theme.getFont("default")
    renderType: Text.NativeRendering

    MouseArea
    {
        anchors.fill: parent
        hoverEnabled: true
		cursorShape: Qt.PointingHandCursor
		onClicked: {
            Qt.openUrlExternally(link.url)
            Analytics.trackEvent("external_url", "link_clicked")
        }
    }
}
