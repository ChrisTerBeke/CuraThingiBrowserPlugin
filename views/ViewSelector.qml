import QtQuick 2.2
import QtQuick.Controls 2.0
import QtQuick.Dialogs 1.1
import QtQuick.Layouts 1.3
import QtQuick.Window 2.2
import QtGraphicalEffects 1.0 // For the dropshadow
import UM 1.1 as UM
import Cura 1.0 as Cura

Cura.ExpandablePopup
{
    id: viewSelector
    implicitHeight: parent.height
    implicitWidth: 200 * screenScaleFactor
    headerPadding: 20
    contentPadding: 0
    headerBackgroundColor: UM.Theme.getColor("main_background")
    headerHoverColor: UM.Theme.getColor("toolbar_button_hover")
    contentBackgroundColor: UM.Theme.getColor("main_background")
    contentAlignment: Cura.ExpandablePopup.ContentAlignment.AlignLeft

    property string labelText: "Custom Search"

    function setAndToggle(selectedName) {
        viewSelector.toggleContent()
        labelText = selectedName
    }

    headerItem: Label
    {
        id: viewSelectorLabel
        text: viewSelector.labelText
        color: UM.Theme.getColor("text")
        font: UM.Theme.getFont("medium")
        verticalAlignment: Qt.AlignVCenter
    }

    contentItem: ColumnLayout
    {
        id: contentContainer
        spacing: 0

        ViewButton
        {
            text: "My Likes"
            backgroundColor: UM.Theme.getColor("main_background")
            onClicked: {
                viewSelector.setAndToggle(text)
                ThingiService.getLiked()
            }
        }

        ViewButtonSeparator { /* No Attributes Needed */ }

        ViewButton
        {
            text: "My Collections"
            backgroundColor: UM.Theme.getColor("main_background")
            onClicked: {
                viewSelector.setAndToggle(text)
                ThingiService.getCollections()
            }
        }

        ViewButtonSeparator { /* No Attributes Needed */ }

        ViewButton
        {
            text: "Popular"
            backgroundColor: UM.Theme.getColor("main_background")
            onClicked: {
                viewSelector.setAndToggle(text)
                ThingiService.getPopular()
                Analytics.trackEvent("get_popular", "button_clicked")
            }
        }

        ViewButtonSeparator { /* No Attributes Needed */ }

        ViewButton
        {
            text: "Featured"
            backgroundColor: UM.Theme.getColor("main_background")
            onClicked: {
                viewSelector.setAndToggle(text)
                ThingiService.getFeatured()
                Analytics.trackEvent("get_featured", "button_clicked")
            }
        }

        ViewButtonSeparator { /* No Attributes Needed */ }

        ViewButton
        {
            text: "Newest"
            backgroundColor: UM.Theme.getColor("main_background")
            onClicked: {
                viewSelector.setAndToggle(text)
                ThingiService.getNewest()
                Analytics.trackEvent("get_newest", "button_clicked")
            }
        }

        ViewButtonSeparator { /* No Attributes Needed */ }
    }

    Component.onCompleted: {
        contentContainer.width = viewSelector.width + viewSelector.anchors.margins
    }
}
