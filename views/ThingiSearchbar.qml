import QtQuick 2.0
import QtQuick.Controls 2.0
import QtQuick.Layouts 1.3
import UM 1.1 as UM
import Cura 1.0 as Cura

Item {
    id: searchbar

    RowLayout {
        anchors.fill: parent
        spacing: 0

        ViewSelector {
            id: serviceSelector
            headerRadius: 5
            headerCornerSide: 4
            enableHeaderShadow: false
            anchors.top: parent.top
            anchors.bottom: parent.bottom
            anchors.margins: searchbarBackground.border.width
            Layout.margins: searchbarBackground.border.width

            property string headerImageSource: "thingiverse-logo-2015.png"

            function setHeaderImageSource(value) {
                serviceSelector.toggleContent()
                headerImageSource = value
            }

            headerItem:  Item {
                id: serviceSelectorHeader

                Image {
                    id: serviceSelectorImage
                    source: serviceSelector.headerImageSource
                    cache: false
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    fillMode: Image.PreserveAspectFit
                    Layout.margins: UM.Theme.getSize("default_margin").width
                            
                }
            }

            contentItem: ColumnLayout {
                id: contentContainer

                ViewButton {
                    id: thingiverseButton
                    width: serviceSelectorHeader.width
                    height: serviceSelectorHeader.height
                    background: Item {
                        Rectangle {
                            height: parent.height
                            width: parent.width
                            color: UM.Theme.getColor("main_background")
                            radius: 0
                            anchors.fill: parent
                        }

                        Image {
                            id: thingiverseLogo
                            Layout.fillWidth: true
                            Layout.fillHeight: true
                            fillMode: Image.PreserveAspectFit
                            anchors.fill: parent
                            anchors.margins: UM.Theme.getSize("default_margin").width
                            source: "thingiverse-logo-2015.png"
                        }
                    }
                    onClicked: {
                        serviceSelector.setHeaderImageSource(thingiverseLogo.source)
                        ThingiService.setService("Thingiverse")
                    }
                }

                ViewButtonSeparator { /* No Attributes Needed */ }

                ViewButton {
                    id: myMiniFactoryButton
                    width: serviceSelectorHeader.width
                    height: serviceSelectorHeader.height
                    background: Item {
                        Rectangle {
                            height: parent.height
                            width: parent.width
                            color: UM.Theme.getColor("main_background")
                            radius: 0
                            anchors.fill: parent
                        }

                        Image {
                            id: myMiniFactoryLogo
                            Layout.fillWidth: true
                            Layout.fillHeight: true
                            fillMode: Image.PreserveAspectFit
                            anchors.fill: parent
                            anchors.margins: UM.Theme.getSize("default_margin").width
                            source: "my-mini-factory-logo-dropshadow.png"
                        }
                    }
                    onClicked: {
                        serviceSelector.setHeaderImageSource(myMiniFactoryLogo.source)
                        ThingiService.setService("MyMiniFactory")
                    }
                }
            }

            Component.onCompleted: {
                contentContainer.width = serviceSelector.width + serviceSelector.anchors.margins
            }
        }

        // Separator line
        Rectangle {
            height: parent.height - 2 // for some reason the parent height results in a too tall separator
            width: UM.Theme.getSize("default_lining").width
            color: UM.Theme.getColor("lining")
        }

        TextField {
            id: thingSearchField
            placeholderText: "Search for things..."
            Layout.alignment: Qt.AlignCenter
            Layout.fillWidth: true
            Layout.rightMargin: UM.Theme.getSize("default_margin").width
            onAccepted: {
                viewSelector.labelText = "Search"
                ThingiService.search(thingSearchField.text)
                Analytics.trackEvent("search_field", "enter_pressed")
            }
            selectByMouse: true
        }

        Cura.PrimaryButton {
            text: "Search"
            onClicked: {
                viewSelector.labelText = "Search"
                ThingiService.search(thingSearchField.text)
                Analytics.trackEvent("search_field", "button_clicked")
            }
            Layout.alignment: Qt.AlignCenter
            Layout.rightMargin: UM.Theme.getSize("default_margin").width
        }

        // Separator line
        Rectangle {
            height: parent.height - 2 // for some reason the parent height results in a too tall separator
            width: UM.Theme.getSize("default_lining").width
            color: UM.Theme.getColor("lining")
        }

        ViewSelector {
            id: viewSelector
            headerRadius: 5
            headerCornerSide: 4
            enableHeaderShadow: false
            anchors.top: parent.top
            anchors.bottom: parent.bottom
            anchors.margins: searchbarBackground.border.width
            Layout.margins: searchbarBackground.border.width
        }
    }

    Rectangle {
        id: searchbarBackground
        height: parent.height
        width: parent.width
        color: UM.Theme.getColor("main_background")
        border.color: UM.Theme.getColor("lining")
        radius: UM.Theme.getSize("default_radius").width
        z: parent.z - 1
    }
}

/*##^##
Designer {
    D{i:0;autoSize:true;height:480;width:640}
}
##^##*/
