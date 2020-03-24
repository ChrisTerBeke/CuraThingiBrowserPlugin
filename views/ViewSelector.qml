import QtQuick 2.2
import QtQuick.Controls 2.3

ComboBox
{
    textRole: "text"
    currentIndex: -1
    model: ListModel {
        id: viewsListModel
        ListElement {
            text: "My Likes"
            value: "userLikes"
        }
        ListElement {
            text: "My Collections"
            value: "userCollections"
        }
        ListElement {
            text: "My Things"
            value: "userThings"
        }
        ListElement {
            text: "My Makes"
            value: "userMakes"
        }
        ListElement {
            text: "Popular"
            value: "popular"
        }
        ListElement {
            text: "Featured"
            value: "featured"
        }
        ListElement {
            text: "Newest"
            value: "newest"
        }
    }
    onActivated: {
        switch(viewsListModel.get(currentIndex).value) {
            case "userLikes":
                ThingiService.getLiked()
                Analytics.trackEvent("get_user_likes", "button_clicked")
                break
            case "userCollections":
                ThingiService.getCollections()
                Analytics.trackEvent("get_user_collections", "button_clicked")
                break
            case "userThings":
                ThingiService.getMyThings()
                Analytics.trackEvent("get_user_things", "button_clicked")
                break
            case "userMakes":
                ThingiService.getMakes()
                Analytics.trackEvent("get_user_makes", "button_clicked")
                break
            case "popular":
                ThingiService.getPopular()
                Analytics.trackEvent("get_popular", "button_clicked")
                break
            case "featured":
                ThingiService.getFeatured()
                Analytics.trackEvent("get_featured", "button_clicked")
                break
            case "newest":
                ThingiService.getNewest()
                Analytics.trackEvent("get_newest", "button_clicked")
        }
    }
}
