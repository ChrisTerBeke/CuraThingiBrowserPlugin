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
    height: UM.Theme.getSize("toolbox_header").height
    color: "#f5f5f5"

    RowLayout
    {
        height: parent.height
        width: parent.width

        Image
        {
            sourceSize.width: 100
            source: "thingiverse-logo-2015.png"
            Layout.leftMargin: 20
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
            Layout.preferredWidth: parent.width / 4
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

        Item
        {
            Layout.fillWidth: true // create some space between the search section and the other buttons
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
            Layout.rightMargin: 20 // we need some padding from the right edge of the window
        }
    }
}
