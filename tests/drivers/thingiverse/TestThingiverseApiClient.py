# Copyright (c) 2020.
# Thingiverse plugin is released under the terms of the LGPLv3 or higher.
from unittest.mock import patch

import pytest
from surrogate import surrogate


API_CALL_TIMEOUT = 10000


class TestThingiverseApiClient:

    @pytest.fixture
    @surrogate("cura.CuraApplication.CuraApplication")
    @surrogate("UM.Signal.Signal")
    def api_client(self, application):
        with patch("cura.CuraApplication.CuraApplication", application):
            from ....ThingiBrowser.drivers.thingiverse.ThingiverseApiClient import ThingiverseApiClient
            return ThingiverseApiClient()

    def test_getThingsFromCollectionQuery(self, api_client):
        query = api_client.getThingsFromCollectionQuery("my-collection")
        assert query == "collections/my-collection/things"

    def test_getThingsBySearchQuery(self, api_client):
        query = api_client.getThingsBySearchQuery("cube")
        assert query == "search/cube"

    def test_getThingsLikedByUserQuery(self, api_client):
        query = api_client.getThingsLikedByUserQuery()
        assert query == "users/404_this_user_does_not_exist/likes"

    def test_getThingsByUserQuery(self, api_client):
        query = api_client.getThingsByUserQuery()
        assert query == "users/404_this_user_does_not_exist/things"

    def test_getThingsMadeByUserQuery(self, api_client):
        query = api_client.getThingsMadeByUserQuery()
        assert query == "users/404_this_user_does_not_exist/copies"

    def test_getPopularThingsQuery(self, api_client):
        query = api_client.getPopularThingsQuery()
        assert query == "popular"

    def test_getFeaturedThingsQuery(self, api_client):
        query = api_client.getFeaturedThingsQuery()
        assert query == "featured"

    def test_getNewestThingsQuery(self, api_client):
        query = api_client.getNewestThingsQuery()
        assert query == "newest"
