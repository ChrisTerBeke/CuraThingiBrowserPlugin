# Copyright (c) 2020.
# ThingiBrowser plugin is released under the terms of the LGPLv3 or higher.
from unittest.mock import MagicMock, patch, DEFAULT

import pytest
import requests
from surrogate import surrogate
from typing import Callable


class SignalMock(MagicMock):

    def connect(self, callback: Callable) -> None:
        pass

    def emit(self, *args, **kwargs) -> None:
        pass


class TestLocalAuthService:

    @pytest.fixture(scope="session")
    @surrogate("UM.Signal.Signal")
    def auth_service(self):
        with patch("UM.Signal.Signal", SignalMock):
            from ...ThingiBrowser.api.LocalAuthService import LocalAuthService
            auth_service = LocalAuthService()
            auth_service.start("https://ultimaker.com")
            return auth_service

    def test_server_callback_url(self, auth_service):
        response = requests.get("http://localhost:55444/callback#access_token=derp&state=hi")
        assert response.status_code == 200

    def test_server_redirected_callback_url(self, auth_service):
        with patch.multiple(SignalMock, connect=DEFAULT, emit=DEFAULT) as mocked_signal:
            response = requests.get("http://localhost:55444/callback?access_token=derp&state=hi")
            assert response.status_code == 200
            mocked_signal["emit"].assert_called_with("hi", "derp")

    def test_server_invalid_url(self, auth_service):
        response = requests.get("http://localhost:55444/derp")
        assert response.status_code == 404
