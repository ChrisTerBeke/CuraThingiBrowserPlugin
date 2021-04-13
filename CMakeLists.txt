cmake_minimum_required(VERSION 3.20)
project(ThingiBrowser)

# All the Python files we want to ship in our built plugin
set(python_files
    __init__.py
    ThingiBrowser/__init__.py
    ThingiBrowser/PreferencesHelper.py
    ThingiBrowser/Settings.py
    ThingiBrowser/ThingiBrowserExtension.py
    ThingiBrowser/ThingiBrowserService.py
    ThingiBrowser/api/__init__.py
    ThingiBrowser/api/AbstractApiClient.py
    ThingiBrowser/api/Analytics.py
    ThingiBrowser/api/ApiHelper.py
    ThingiBrowser/api/ImplicitAuthRequestHandler.py
    ThingiBrowser/api/JsonObject.py
    ThingiBrowser/api/LocalAuthService.py
    ThingiBrowser/drivers/myminifactory/__init__.py
    ThingiBrowser/drivers/myminifactory/MyMiniFactoryApiClient.py
    ThingiBrowser/drivers/thingiverse/__init__.py
    ThingiBrowser/drivers/thingiverse/ThingiverseApiClient.py
    ThingiBrowser/models/__init__.py
    ThingiBrowser/models/DriverOption.py
    ThingiBrowser/models/ViewOption.py
)

# All the QML (UI) files we want to ship in our built plugin
set(qml_files
    views/EnhancedButton.qml
    views/EnhancedComboBox.qml
    views/EnhancedTextField.qml
    views/Link.qml
    views/ServiceSelector.qml
    views/ThingDetailsPage.qml
    views/ThingFilesList.qml
    views/ThingFilesListItem.qml
    views/ThingSearchPage.qml
    views/ThingiHeader.qml
    views/ThingiMain.qml
    views/ThingiSearchbar.qml
    views/ThingiSettings.qml
    views/ThingiSettingsItem.qml
    views/Thingiverse.qml
    views/ThingsList.qml
    views/ThingsListItem.qml
    views/ViewSelector.qml
)

# All the extra assets we want to ship in our built plugin
set(asset_files
    LICENSE
    plugin.json
    ThingiBrowser/static/AuthenticationReceived.html
    ThingiBrowser/static/AuthenticationRedirect.html
    views/images/loading.gif
)

# Combine all files
set(all_files "")
list(APPEND all_files ${python_files})
list(APPEND all_files ${qml_files})
list(APPEND all_files ${asset_files})

# Generate the ZIP file that we can upload in the Ultimaker contributor portal
foreach(file ${all_files})
    get_filename_component(dir ${file} DIRECTORY)
    install(FILES ${file} DESTINATION ${CMAKE_PROJECT_NAME}/${dir})
endforeach()
set(CPACK_GENERATOR "ZIP")
set(CPACK_PACKAGE_FILE_NAME ${CMAKE_PROJECT_NAME})
set(CPACK_INCLUDE_TOPLEVEL_DIRECTORY OFF)
set(CPACK_VERBATIM_VARIABLES YES)
include(CPack)
