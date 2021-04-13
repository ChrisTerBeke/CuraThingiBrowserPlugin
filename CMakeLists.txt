cmake_minimum_required(VERSION 3.20)
project(ThingiBrowser)

# All the Python files we want to ship in our built plugin
set(python_files
    ThingiBrowser/__init__.py
    ThingiBrowser/PreferencesHelper.py
    ThingiBrowser/Settings.py
    ThingiBrowser/ThingiBrowserExtension.py
    ThingiBrowser/ThingiBrowserService.py
    ThingiBrowser/api/__init__.py
    ThingiBrowser/api/AbstractClient.py
    ThingiBrowser/api/Analytics.py
    ThingiBrowser/api/ApiHelper.py
    ThingiBrowser/api/ImplicitAuthRequestHandler.py
    ThingiBrowser/api/JsonObject.py
    ThingiBrowser/api/LocalAuthService.py
    ThingiBrowser/drivers/myminifactory/__init__.py
    ThingiBrowser/drivers/myminifactory/MyMiniFactoryApiClient.py
    ThingiBrowser/drivers/thingiverse/__init__.py
    ThingiBrowser/drivers/thingiverse/ThingiverseApiClient.py
    ThingiBrowser/models/__init.py
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
foreach(f IN LISTS python_files)
	list(APPEND all_files ${CMAKE_CURRENT_SOURCE_DIR}/${f})
endforeach()
foreach(f IN LISTS qml_files)
	list(APPEND all_files ${CMAKE_CURRENT_SOURCE_DIR}/${f})
endforeach()
foreach(f IN LISTS asset_files)
	list(APPEND all_files ${CMAKE_CURRENT_SOURCE_DIR}/${f})
endforeach()

# Generate the ZIP file that we can upload in the Ultimaker contributor portal
add_custom_target(create_zip COMMAND
    ${CMAKE_COMMAND} -E tar "cfv" "thingibrowser.zip" --format=zip -- ${all_files}
)
