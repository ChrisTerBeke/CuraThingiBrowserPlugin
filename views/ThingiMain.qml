// Copyright (c) 2020.
// Thingiverse plugin is released under the terms of the LGPLv3 or higher.
import QtQuick
import QtQuick.Controls
import QtQuick.Dialogs
import QtQuick.Layouts
import QtQuick.Window
import UM 1.1 as UM

ColumnLayout {
    anchors.fill: parent

    // the header
    ThingiHeader {
        Layout.alignment: Qt.AlignTop
    }

    // the search page
    ThingSearchPage {
        width: parent.width
        visible: !ThingiService.hasActiveThing
        Layout.fillHeight: true
        onVisibleChanged: {
            if (visible) {
                Analytics.trackScreen("search")
            }
        }
    }

    // the details page
    ThingDetailsPage {
        width: parent.width
        thing: ThingiService.hasActiveThing ? ThingiService.activeThing : null
        thingFiles: ThingiService.hasActiveThing ? ThingiService.activeThingFiles : []
        visible: ThingiService.hasActiveThing
        Layout.fillHeight: true
        onVisibleChanged: {
            if (visible) {
                Analytics.trackScreen("details")
            }
        }
    }
}
