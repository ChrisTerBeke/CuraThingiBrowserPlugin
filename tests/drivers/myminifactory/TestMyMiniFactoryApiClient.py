# Copyright (c) 2020.
# Thingiverse plugin is released under the terms of the LGPLv3 or higher.
from unittest.mock import patch

import pytest
from surrogate import surrogate

from ....ThingiBrowser.api.JsonObject import UserData

API_CALL_TIMEOUT = 10000


class TestMyMiniFactoryApiClient:

    @pytest.fixture
    @surrogate("cura.CuraApplication.CuraApplication")
    @surrogate("UM.Signal.Signal")
    def api_client(self, application):
        with patch("cura.CuraApplication.CuraApplication", application):
            from ....ThingiBrowser.drivers.myminifactory.MyMiniFactoryApiClient import MyMiniFactoryApiClient
            return MyMiniFactoryApiClient()

    def test_getThingsFromCollectionQuery(self, api_client):
        query = api_client.getThingsFromCollectionQuery("my-collection")
        assert query == "collections/my-collection"

    def test_getThingsBySearchQuery(self, api_client):
        query = api_client.getThingsBySearchQuery("cube")
        assert query == "search?q=cube"

    def test_getThingsLikedByUserQuery(self, api_client):
        api_client._onGetUserData(UserData({"username": "herpaderp"}))
        query = api_client.getThingsLikedByUserQuery()
        assert query == "users/herpaderp/objects_liked"

    def test_getThingsByUserQuery(self, api_client):
        api_client._onGetUserData(UserData({"username": "herpaderp"}))
        query = api_client.getThingsByUserQuery()
        assert query == "users/herpaderp/objects"

    def test_getThingsMadeByUserQuery(self, api_client):
        api_client._onGetUserData(UserData({"username": "herpaderp"}))
        query = api_client.getThingsMadeByUserQuery()
        assert query == "users/herpaderp/objects"

    def test_getThingsMadeByUserQuery_not_authenticated(self, api_client):
        query = api_client.getThingsMadeByUserQuery()
        assert query == "users/None/objects"

    def test_getPopularThingsQuery(self, api_client):
        query = api_client.getPopularThingsQuery()
        assert query == "search?sort=popularity"

    def test_getFeaturedThingsQuery(self, api_client):
        query = api_client.getFeaturedThingsQuery()
        assert query == "search?featured=1"

    def test_getNewestThingsQuery(self, api_client):
        query = api_client.getNewestThingsQuery()
        assert query == "search?sort=date"
