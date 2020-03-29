# Copyright (c) 2020 Chris ter Beke.
# Thingiverse plugin is released under the terms of the LGPLv3 or higher.
import os
import pathlib
import tempfile
from typing import List, Optional, TYPE_CHECKING, Dict, Any, cast

from PyQt5.QtCore import QObject, pyqtProperty, pyqtSignal, pyqtSlot, QUrl  # type: ignore
from PyQt5.QtWidgets import QMessageBox

from cura.CuraApplication import CuraApplication  # type: ignore

from .PreferencesHelper import PreferencesHelper
from .api.AbstractApiClient import AbstractApiClient
from .api.JsonObject import Thing, ThingFile, Collection, ApiError
from .drivers.thingiverse.ThingiverseApiClient import ThingiverseApiClient
from .drivers.myminifactory.MyMiniFactoryApiClient import MyMiniFactoryApiClient
from .Settings import Settings

if TYPE_CHECKING:
    from .ThingiBrowserExtension import ThingiBrowserExtension


class ThingiBrowserService(QObject):
    """
    The ThingiverseService uses the API client to serve Thingiverse content to the UI.
    """

    # Signal triggered when new things are found.
    thingsChanged = pyqtSignal()

    # Signal triggered when the from collection state changed.
    isFromCollectionChanged = pyqtSignal()

    # Signal triggered the value of a setting changed.
    settingChanged = pyqtSignal(str, str)

    # Signal triggered when the querying state changed.
    queryingStateChanged = pyqtSignal()

    # Signal triggered when the active thing changed.
    activeThingChanged = pyqtSignal()

    # Signal triggered when the active thing files changed.
    activeThingFilesChanged = pyqtSignal()

    # Signal triggered when a file has started or stopped downloading.
    downloadingStateChanged = pyqtSignal()

    # Signal triggered when the active API driver is changed.
    activeDriverChanged = pyqtSignal()

    def __init__(self, extension: "ThingiBrowserExtension", parent=None):
        super().__init__(parent)
        self._extension = extension  # type: ThingiBrowserExtension

        # List of supported file types.
        self._supported_file_types = []  # type: List[str]

        # Hold the things found in query results.
        self._things = []  # type: List[Thing]
        self._query = ""  # type: str
        self._query_page = 1  # type: int
        self._is_querying = False  # type: bool
        self._is_from_collection = False  # type: bool

        # Hold the thing and thing files that we currently see the details of.
        self._thing_details = None  # type: Optional[Thing]
        self._thing_files = []  # type: List[ThingFile]
        self._is_downloading = False  # type: bool

        # Drivers for the services we can interact with.
        self._drivers = {
            "thingiverse": ThingiverseApiClient(),
            "myminifactory": MyMiniFactoryApiClient(),
        }  # type: Dict[str, AbstractApiClient]
        self._active_driver_name = PreferencesHelper.initSetting(Settings.DEFAULT_API_CLIENT, "thingiverse")  # type: str
        self.activeDriverChanged.connect(self._onDriverChanged)

    def resetActiveDriver(self) -> None:
        """
        Reset the active driver to the one selected as deafult
        """
        self.setActiveDriver(PreferencesHelper.getSettingValue(Settings.DEFAULT_API_CLIENT))

    def updateSupportedFileTypes(self) -> None:
        """
        Refresh the available file types (triggered when plugin window is loaded).
        """
        supported_file_types = CuraApplication.getInstance().getMeshFileHandler().getSupportedFileTypesRead()
        self._supported_file_types = list(supported_file_types.keys())

    def runDefaultQuery(self) -> None:
        """
        Run the default query that searches for items with the keyword 'ultimaker'.
        """
        self.search("ultimaker")

    @pyqtProperty(list, notify=settingChanged)
    def getSettings(self) -> List[Dict[str, Any]]:
        """
        Get all the available settings so the UI can display them.
        :return: The settings.
        """
        return PreferencesHelper.getAllSettings()

    @pyqtSlot(str, str, name="saveSetting")
    def setSetting(self, setting_name: str, value: str) -> None:
        """
        Change the value of a setting.
        :param setting_name: The name of the setting.
        :param value: The new value.
        """
        PreferencesHelper.setSetting(setting_name, value)
        self.settingChanged.emit(setting_name, value)

    @pyqtSlot(name="openSettings")
    def openSettings(self) -> None:
        """ Open the settings window. """
        if not self._extension:
            return
        self._extension.showSettingsWindow()

    @pyqtProperty("QVariantList", constant=True)
    def drivers(self) -> List[Dict[str, str]]:
        """
        Get the available drivers for selecting in the UI.
        :return: The drivers.
        """
        return Settings.DRIVERS

    @pyqtProperty(str, notify=activeDriverChanged)
    def activeDriver(self) -> str:
        """
        Return the key of the active driver
        :return: The active driver key
        """
        return self._active_driver_name

    @pyqtSlot(str, name="setActiveDriver")
    def setActiveDriver(self, driver: str) -> None:
        """
        Set the active API driver.
        Checks if the selected driver is actually available.
        :param driver: The name of the driver to activate.
        """
        if driver == self._active_driver_name:
            return
        if driver not in self._drivers:
            return
        self._active_driver_name = driver
        self.activeDriverChanged.emit()

    @pyqtProperty(list, notify=activeDriverChanged)
    def availableViews(self) -> List[str]:
        """
        Get any disabled views for the current API driver.
        :return: List of views that should be visible.
        """
        return self._getActiveDriver().available_views

    @pyqtProperty("QVariantList", notify=thingsChanged)
    def things(self) -> List[Dict[str, Any]]:
        """
        Get a list of found things. Updated when performing a search.
        :return: The things.
        """
        return [thing.toStruct() for thing in self._things]

    @pyqtProperty(bool, notify=isFromCollectionChanged)
    def isFromCollection(self) -> bool:
        """
        Whether the current list of results is a user collection or not.
        :return: True if from collection, False otherwise.
        """
        return self._is_from_collection

    @pyqtProperty(bool, notify=queryingStateChanged)
    def isQuerying(self) -> bool:
        """
        Whether we're currently waiting for an API response or not.
        :return: True if waiting, False otherwise.
        """
        return self._is_querying

    @pyqtProperty("QVariantMap", notify=activeThingChanged)
    def activeThing(self) -> Optional[Dict[str, Any]]:
        """
        Get the current active thing details.
        :return: The thing.
        """
        return self._thing_details.toStruct() if self._thing_details else None

    @pyqtProperty("QVariantList", notify=activeThingFilesChanged)
    def activeThingFiles(self) -> List[Dict[str, Any]]:
        """
        Get the current active thing files.
        :return: The thing files.
        """
        return [files.toStruct() for files in self._thing_files]

    @pyqtProperty(bool, notify=activeThingChanged)
    def hasActiveThing(self) -> bool:
        """
        Whether there is currently a thing active to show or not.
        :return: True when there is an active thing, false otherwise.
        """
        return bool(self._thing_details)

    @pyqtProperty(bool, notify=downloadingStateChanged)
    def isDownloading(self) -> bool:
        """
        Whether there is currently a download in progress or not.
        :return: True if currently downloading, false otherwise.
        """
        return self._is_downloading

    @pyqtSlot(str, name="search")
    def search(self, search_term: str) -> None:
        """
        Search for things by search term.
        :param search_term: What to search for.
        """
        query = self._getActiveDriver().getThingsBySearchQuery(search_term)
        self._executeQuery(query)

    @pyqtSlot(name="getLiked")
    def getLiked(self) -> None:
        """
        Get the current user's liked things.
        """
        if not self._checkUserNameConfigured():
            return
        query = self._getActiveDriver().getThingsLikedByUserQuery()
        self._executeQuery(query)

    @pyqtSlot(name="getMyThings")
    def getMyThings(self) -> None:
        """
        Get the current user's published Things.
        """
        if not self._checkUserNameConfigured():
            return
        query = self._getActiveDriver().getThingsByUserQuery()
        self._executeQuery(query)

    @pyqtSlot(name="getMakes")
    def getMakes(self) -> None:
        """
        Get the current user's made Things.
        """
        if not self._checkUserNameConfigured():
            return
        query = self._getActiveDriver().getThingsMadeByUserQuery()
        self._executeQuery(query)

    @pyqtSlot(name="getPopular")
    def getPopular(self) -> None:
        """
        Get the most popular things.
        The result is async and will be populated in self._things.
        """
        query = self._getActiveDriver().getPopularThingsQuery()
        self._executeQuery(query)

    @pyqtSlot(name="getFeatured")
    def getFeatured(self) -> None:
        """
        Get the featured things.
        The result is async and will be populated in self._things.
        """
        query = self._getActiveDriver().getFeaturedThingsQuery()
        self._executeQuery(query)

    @pyqtSlot(name="getNewest")
    def getNewest(self) -> None:
        """
        Get the newest things.
        The result is async and will be populated in self._things.
        """
        query = self._getActiveDriver().getNewestThingsQuery()
        self._executeQuery(query)

    @pyqtSlot(name="getCollections")
    def getCollections(self) -> None:
        """
        Get the current user's collections.
        """
        if not self._checkUserNameConfigured():
            return
        self._prepQuery("user_collections", is_from_collection=False)
        self._getActiveDriver().getCollections(on_finished=self._onCollectionsFinished, on_failed=self._onRequestFailed)

    @pyqtSlot(int, name="showCollectionDetails")
    def showCollectionDetails(self, collection_id: int) -> None:
        """
        Get and show the details of a single collection.
        :param collection_id: The ID of the collection.
        """
        query = self._getActiveDriver().getThingsFromCollectionQuery(str(collection_id))
        self._executeQuery(query, is_from_collection=True)

    @pyqtSlot(int, name="showThingDetails")
    def showThingDetails(self, thing_id: int) -> None:
        """
        Get and show the details of a single thing.
        :param thing_id: The ID of the thing.
        """
        self._getActiveDriver().getThing(thing_id, self._onThingDetailsFinished, on_failed=self._onRequestFailed)
        self._getActiveDriver().getThingFiles(thing_id, self._onThingFilesFinished, on_failed=self._onRequestFailed)

    @pyqtSlot(name="hideThingDetails")
    def hideThingDetails(self) -> None:
        """
        Remove the thing details. This hides the detail page in the UI.
        """
        self._thing_details = None
        self.activeThingChanged.emit()

    @pyqtSlot(int, str, name="downloadThingFile")
    def downloadThingFile(self, file_id: int, file_name: str) -> None:
        """
        Download and load a thing file by it's ID.
        The downloaded object will be placed on the build plate.
        :param file_id: The ID of the file.
        :param file_name: The name of the file.
        """
        self._is_downloading = True
        self.downloadingStateChanged.emit()
        self._getActiveDriver().downloadThingFile(file_id, file_name,
                                                  on_finished=lambda data: self._onDownloadFinished(data, file_name))

    @pyqtProperty(int, notify=thingsChanged)
    def currentPage(self) -> int:
        """
        Get the current query results page.
        :return: The page number, starting with 1.
        """
        return self._query_page

    @pyqtSlot(name="previousPage")
    def previousPage(self) -> None:
        """
        Navigate to the previous page of query results.
        The search is done async and the result will be populated in self._things.
        Can not go lower than page 1.
        """
        if self._query_page == 1:
            return
        self._query_page -= 1
        self._executeQuery(is_from_collection=self._is_from_collection)

    @pyqtSlot(name="nextPage")
    def nextPage(self) -> None:
        """
        Navigate to the next page of query results.
        The search is done async and the result will be populated in self._things.
        """
        self._query_page += 1
        self._executeQuery(is_from_collection=self._is_from_collection)

    def _executeQuery(self, new_query: Optional[str] = None, is_from_collection: Optional[bool] = False) -> None:
        """
        Internal function to query the API for things.
        :param new_query: Perform a new query instead of adding a new page to the existing one.
        :param is_from_collection: Specifies whether the resulting Things are part of a collection or not.
        """
        self._prepQuery(new_query, is_from_collection)
        self._getActiveDriver().getThings(query=self._query, page=self._query_page, on_finished=self._onQueryFinished,
                                          on_failed=self._onRequestFailed)

    def _prepQuery(self, new_query: Optional[str] = None, is_from_collection: Optional[bool] = False) -> None:
        """
        State configuration that needs to happen before each query.
        :param new_query: Perform a new query instead of adding a new page to the existing one.
        :param is_from_collection: Specifies whether the resulting Things are part of a collection or not.
        """
        if new_query:
            self._query = new_query
            self._clearSearchResults()
            self._query_page = 1
        if self._is_from_collection != is_from_collection:
            self._is_from_collection = bool(is_from_collection)
            self.isFromCollectionChanged.emit()
        self._is_querying = True
        self.queryingStateChanged.emit()

    def _onThingDetailsFinished(self, thing: Thing) -> None:
        """
        Callback for receiving thing details on.
        :param thing: The thing.
        """
        self._thing_details = thing
        self.activeThingChanged.emit()

    def _onThingFilesFinished(self, thing_files: List[ThingFile]) -> None:
        """
        Callback for receiving a list of thing files on. Filtered on supported file types of Cura.
        :param thing_files: The thing files.
        """
        self._thing_files = []
        for file in thing_files:
            if file.name and pathlib.Path(file.name).suffix.lower().strip(".") in self._supported_file_types:
                self._thing_files.append(file)
        self.activeThingFilesChanged.emit()

    def _onDownloadFinished(self, file_bytes: bytes, file_name: str) -> None:
        """
        Callback to receive the downloaded file on and import it onto the build plate.
        Note that we do not use any context clauses here. Even though that would be cleaner,
        CuraApplication.getInstance() switches contexts and makes temporary dirs and files be removed by their context.
        :param file_bytes: The file as bytes.
        :param file_name: The file name.
        """
        file_path = os.path.join(tempfile.mkdtemp(), file_name)
        tmp_file = open(file_path, "wb")
        tmp_file.write(file_bytes)
        tmp_file.close()
        CuraApplication.getInstance().readLocalFile(QUrl().fromLocalFile(tmp_file.name))
        self._is_downloading = False
        self.downloadingStateChanged.emit()

    def _onQueryFinished(self, things: List[Thing]) -> None:
        """
        Callback for receiving thing results on.
        :param things: The found things.
        """
        self._is_querying = False
        self.queryingStateChanged.emit()
        self._things = things
        self.thingsChanged.emit()

    def _onCollectionsFinished(self, collections: List[Collection]) -> None:
        """
        Callback for receiving collections results on.
        :param collections: The found collections.
        """
        self._is_querying = False
        self.queryingStateChanged.emit()
        self._things = cast(List[Thing], collections)  # we know that Thing and Collection are compatible, MyPy does not
        self.thingsChanged.emit()

    def _clearSearchResults(self) -> None:
        """
        Clear all Thing search results.
        """
        self._things = []
        self._query_page = 1
        self.hideThingDetails()
        self.thingsChanged.emit()

    def _onDriverChanged(self) -> None:
        """
        Execute default search query when driver changes.
        This is needed to prevent compatibility issues with the cached query.
        """
        self.runDefaultQuery()

    def _onRequestFailed(self, error: Optional[ApiError] = None) -> None:
        """
        Callback for when a request failed.
        :param error: An optional error object that was returned by the Thingiverse API.
        """
        self._is_querying = False
        mb = QMessageBox()
        mb.setIcon(QMessageBox.Critical)
        mb.setWindowTitle("Oh no!")
        error_message = error.error or str(error) if error else "Unknown"
        mb.setText("The API returned an error: {}.".format(error_message))
        mb.setDetailedText(str(error.toStruct()) if error else "")
        mb.exec()

    def _checkUserNameConfigured(self) -> bool:
        """
        Checks if the username setting was configured and open the settings window if it was not.
        :return: True if the username was already configured, False otherwise.
        """
        user_id = self._getActiveDriver().user_id
        if not user_id or user_id == "":
            self.openSettings()
            return False
        return True

    def _getActiveDriver(self) -> AbstractApiClient:
        """
        Get the currently active driver.
        Sets the first available driver to active if none was set.
        :return: The active API driver.
        """
        if not self._active_driver_name:
            self._active_driver_name = list(self._drivers.keys())[0]
        return self._drivers[self._active_driver_name]
