# Copyright (c) 2020 Chris ter Beke.
# Thingiverse plugin is released under the terms of the LGPLv3 or higher.
from unittest.mock import patch, MagicMock

import pytest
from surrogate import surrogate


API_CALL_TIMEOUT = 10000


class TestThingiverseApiClient:
    
    @pytest.fixture
    @surrogate("cura.CuraApplication.CuraApplication")
    def api_client(self, application):
        with patch("cura.CuraApplication.CuraApplication", application):
            from ....ThingiBrowser.drivers.thingiverse.ThingiverseApiClient import ThingiverseApiClient
            return ThingiverseApiClient()

    def test_getThingsFromCollectionQuery(self, api_client):
        query = api_client.getThingsFromCollectionQuery("my-collection")
        assert query == "collections/my-collection/things"
        
    def test_getThingsBySearchQuery(self, api_client):
        query = api_client.getThingsBySearchQuery("cube")
        assert query == "search/cube/?sort=relevent"
        
    def test_getThingsLikedByUserQuery(self, api_client):
        query = api_client.getThingsLikedByUserQuery()
        assert query == "users/None/likes"
        
    def test_getThingsByUserQuery(self, api_client):
        query = api_client.getThingsByUserQuery()
        assert query == "users/None/things"
        
    def test_getThingsMadeByUserQuery(self, api_client):
        query = api_client.getThingsMadeByUserQuery()
        assert query == "users/None/copies"
        
    def test_getPopularThingsQuery(self, api_client):
        query = api_client.getPopularThingsQuery()
        assert query == "popular"

    def test_getFeaturedThingsQuery(self, api_client):
        query = api_client.getFeaturedThingsQuery()
        assert query == "featured"
    
    def test_getNewestThingsQuery(self, api_client):
        query = api_client.getNewestThingsQuery()
        assert query == "newest"

    def test_getCollections(self, api_client, qtbot):
        with qtbot.waitCallback(timeout=API_CALL_TIMEOUT) as on_finished:
            api_client.getCollections(on_finished=on_finished)
        assert len(on_finished.args) == 1

    def test_getThings(self, api_client, qtbot):
        with qtbot.waitCallback(timeout=API_CALL_TIMEOUT) as on_finished:
            api_client.getThings(query="popular", page=0, on_finished=on_finished)
        assert len(on_finished.args) == 1

    def test_getThings_error(self, api_client, qtbot):
        with qtbot.waitCallback(timeout=API_CALL_TIMEOUT) as on_failed:
            api_client.getThings(query="wrong_query", page=0, on_finished=MagicMock(), on_failed=on_failed)
        assert len(on_failed.args) == 1
        
    def test_getThing(self, api_client, qtbot):
        with qtbot.waitCallback(timeout=API_CALL_TIMEOUT) as on_finished:
            api_client.getThing(thing_id=11551, on_finished=on_finished)
        assert len(on_finished.args) == 1
        
    def test_getThing_error(self, api_client, qtbot):
        with qtbot.waitCallback(timeout=API_CALL_TIMEOUT) as on_failed:
            api_client.getThing(thing_id=0, on_finished=MagicMock(), on_failed=on_failed)
        assert len(on_failed.args) == 1

    def test_getThingFiles(self, api_client, qtbot):
        with qtbot.waitCallback(timeout=API_CALL_TIMEOUT) as on_finished:
            api_client.getThingFiles(thing_id=11551, on_finished=on_finished)
        assert len(on_finished.args) == 1

    def test_getThingFiles_error(self, api_client, qtbot):
        with qtbot.waitCallback(timeout=API_CALL_TIMEOUT) as on_failed:
            api_client.getThingFiles(thing_id=0, on_finished=MagicMock(), on_failed=on_failed)
        assert len(on_failed.args) == 1

    def test_downloadThingFile(self, api_client, qtbot):
        with qtbot.waitCallback(timeout=API_CALL_TIMEOUT) as on_finished:
            api_client.downloadThingFile(file_id=1, file_name="", on_finished=on_finished)
        assert len(on_finished.args) == 1
