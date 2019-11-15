// Copyright (c) 2018 Chris ter Beke.
// Thingiverse plugin is released under the terms of the LGPLv3 or higher.
import QtQuick 2.2
import QtQuick.Controls 2.0
import QtQuick.Dialogs 1.1
import QtQuick.Layouts 1.3
import QtQuick.Window 2.2
import UM 1.1 as UM
import Cura 1.0 as Cura

// the main window header
Rectangle
{
    id: header

    width: parent.width
    Layout.fillWidth: true
    height: UM.Theme.getSize("toolbox_header").height * 2
    color: "#f5f5f5"

    GridLayout
    {
        columns: 2
        Layout.minimumWidth: parent.width
        Layout.fillWidth: true
        anchors.margins: 20
        anchors.fill: parent

        RowLayout
        {
            id: topLeftCell
            width: parent.width * 2/3

            Image
            {
                sourceSize.width: 100
                source: "thingiverse-logo-2015.png"
                Layout.rightMargin: 20

                // make the header image clickable
                MouseArea
                {
                    anchors.fill: parent
                    onClicked: {
                        ThingiService.search("ultimaker")
                        Analytics.trackEvent("header_image", "clicked")
                    }
                    hoverEnabled: true
                    cursorShape: Qt.PointingHandCursor
                }
            }

            TextField
            {
                id: thingSearchField
                placeholderText: "Search for things..."
                Layout.alignment: Qt.AlignCenter
                Layout.fillWidth: true
                onAccepted: {
                    ThingiService.search(thingSearchField.text)
                    Analytics.trackEvent("search_field", "enter_pressed")
                }
                selectByMouse: true
            }

            Cura.PrimaryButton
            {
                text: "Search"
                onClicked: {
                    ThingiService.search(thingSearchField.text)
                    Analytics.trackEvent("search_field", "button_clicked")
                }
                Layout.alignment: Qt.AlignCenter
            }
        }

        RowLayout
        {
            id: topRightCell

            Item
            {
                Layout.fillWidth: true
            }

            Cura.SecondaryButton
            {
                text: "My Likes"
                onClicked: {
                    ThingiService.getLiked()
                }
                Layout.alignment: Qt.AlignCenter
            }

            Cura.SecondaryButton
            {
                text: "My Collections"
                onClicked: {
                    ThingiService.getCollections()
                }
                Layout.alignment: Qt.AlignCenter
            }

            Cura.SecondaryButton
            {
                iconSource: UM.Theme.getIcon("settings")
                Layout.minimumHeight: parent.height
                onClicked: {
                    ThingiService.openSettings()
                }
                Layout.alignment: Qt.AlignCenter
            }
            
        }

        RowLayout
        {
            id: bottomLeftCell

            Item
            {
                Layout.fillWidth: true
            }
        }

        RowLayout
        {
            id: bottomRightCell

            Item 
            {
                Layout.fillWidth: true
            }

            Cura.SecondaryButton
            {
                text: "Popular"
                onClicked: {
                    ThingiService.getPopular()
                    Analytics.trackEvent("get_popular", "button_clicked")
                }
                Layout.alignment: Qt.AlignCenter
            }

            Cura.SecondaryButton
            {
                text: "Featured"
                onClicked: {
                    ThingiService.getFeatured()
                    Analytics.trackEvent("get_featured", "button_clicked")
                }
                Layout.alignment: Qt.AlignCenter
            }

            Cura.SecondaryButton
            {
                text: "Newest"
                onClicked: {
                    ThingiService.getNewest()
                    Analytics.trackEvent("get_newest", "button_clicked")
                }
                Layout.alignment: Qt.AlignCenter
            }
        }
    }
}
