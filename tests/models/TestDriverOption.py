# Copyright (c) 2020.
# ThingiBrowser plugin is released under the terms of the LGPLv3 or higher.
from unittest.mock import patch

import pytest
from surrogate import surrogate

from ...ThingiBrowser.models.DriverOption import DriverOption


class TestDriverOption:

    @pytest.fixture
    @surrogate("cura.CuraApplication.CuraApplication")
    def api_client(self, application):
        with patch("cura.CuraApplication.CuraApplication", application):
            from ...ThingiBrowser.drivers.thingiverse.ThingiverseApiClient import ThingiverseApiClient
            return ThingiverseApiClient()

    def test_model(self, api_client):
        driver_option = DriverOption(label="Thingies", driver=api_client)
        assert driver_option.label == "Thingies"
        assert driver_option.driver == api_client
