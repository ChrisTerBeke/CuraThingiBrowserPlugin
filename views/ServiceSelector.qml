import QtQuick 2.0
import QtQuick.Controls 2.0
import QtQuick.Layouts 1.3
import UM 1.1 as UM
import Cura 1.0 as Cura

ViewSelector {
    property string headerImageSource: "thingiverse-logo-2015.png"

    function setHeaderImageSource(value) {
        serviceSelector.toggleContent()
        headerImageSource = value
    }

    id: serviceSelector
    headerRadius: 5
    headerCornerSide: Cura.RoundedRectangle.Direction.All
    enableHeaderShadow: false

    headerItem:  Item {
        id: serviceSelectorHeader
        anchors.fill: serviceSelector

        Image {
            id: serviceSelectorImage
            source: serviceSelector.headerImageSource
            cache: false
            fillMode: Image.PreserveAspectFit
            anchors.fill: parent  
        }
    }

    contentItem: ColumnLayout {
        id: contentContainer
        spacing: 0
        anchors { top: serviceSelector.bottom; left: serviceSelector.left; right: serviceSelector.right }

        ServiceButton {
            id: thingiverseButton
            width: parent.width
            height: serviceSelector.height
            backgroundImageSource: "thingiverse-logo-2015.png"
            onClicked: {
                serviceSelector.setHeaderImageSource(thingiverseButton.backgroundImageSource)
                ThingiService.setService("Thingiverse")
            }
        }

        ViewButtonSeparator { /* No Attributes Needed */ }

        ServiceButton {
            id: myMiniFactoryButton
            width: parent.width
            height: serviceSelector.height
            backgroundImageSource: "my-mini-factory-logo-dropshadow-sm.png"
            onClicked: {
                serviceSelector.setHeaderImageSource(myMiniFactoryButton.backgroundImageSource)
                ThingiService.setService("MyMiniFactory")
            }
        }
    }

    Component.onCompleted: {
        contentContainer.width = serviceSelector.width + serviceSelector.anchors.margins
    }
}