// Copyright (c) 2018 Chris ter Beke.
// Thingiverse plugin is released under the terms of the LGPLv3 or higher.
import QtQuick 2.2
import QtQuick.Controls 2.0
import QtQuick.Dialogs 1.1
import QtQuick.Layouts 1.3
import QtQuick.Window 2.2
import UM 1.1 as UM

// the popup window
Window
{
    id: thingiverse

    // window configuration
    color: UM.Theme.getColor("main_background")
    minimumWidth: Math.round(UM.Theme.getSize("modal_window_minimum").width)
    minimumHeight: Math.round(UM.Theme.getSize("modal_window_minimum").height)
    width: minimumWidth
    height: minimumHeight

    // translations
    UM.I18nCatalog
    {
        id: catalog
        name: "thingiverse"
    }

    title: catalog.i18nc("@title", "Thingiverse")

    // area to provide un-focus option for search field
    MouseArea
    {
        anchors.fill: parent
        focus: true

        onClicked: {
            focus = true
        }

        // hot-reload the contenst when pressing <-
        Keys.onPressed: {
            if (event.key == Qt.Key_Left) {
                loader.reload()
            }
        }
    }

    // we use a Loader to be able to hot-reload this content during development
    Loader
    {
        id: loader
        width: parent.width
        height: parent.height
        source: "ThingiMain.qml"

        // trigger a reload and clear the cache
        function reload() {
            source = ""
            CuraApplication.clearQmlCache()
            source = "./ThingiMain.qml"
        }
    }
}
