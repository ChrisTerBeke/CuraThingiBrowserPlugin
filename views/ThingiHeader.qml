import QtQuick 2.2
import QtQuick.Layouts 1.3

// the main window header
RowLayout
{
    width: parent.width
    height: 40
    spacing: 0

    ServiceSelector
    {
        id: serviceSelector
    }

    ViewSelector
    {
        id: viewSelector
    }

    ThingiSearchbar
    {
        id: searchbar
        Layout.fillWidth: true
    }

    //        ConfigButton
    //        {
    //            id: configButton
    //        }
}
