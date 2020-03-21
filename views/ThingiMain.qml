// Copyright (c) 2020 Chris ter Beke.
// Thingiverse plugin is released under the terms of the LGPLv3 or higher.
import QtQuick 2.2
import QtQuick.Controls 2.0
import QtQuick.Dialogs 1.1
import QtQuick.Layouts 1.3
import QtQuick.Window 2.2
import UM 1.1 as UM

ColumnLayout
{
    anchors.fill: parent

    // the header
    ThingiHeader {}

    // dynamic message for all users fetched from API
    Text
    {
        visible: ThingiService.message != ""
        text: ThingiService.message
        width: parent.width
        Layout.leftMargin: 5
        Layout.topMargin: 5
    }

    // the search page
    ThingSearchPage
    {
        width: parent.width
        visible: !ThingiService.hasActiveThing
        Layout.fillHeight: true
        onVisibleChanged: {
            Analytics.trackScreen("search")
        }
    }

    // the details page
    ThingDetailsPage
    {
        width: parent.width
        thing: ThingiService.activeThing
        thingFiles: ThingiService.activeThingFiles
        visible: ThingiService.hasActiveThing
        Layout.fillHeight: true
        onVisibleChanged: {
            Analytics.trackScreen("details")
        }
    }
}
