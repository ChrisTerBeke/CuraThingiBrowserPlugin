# Copyright (c) 2020.
# ThingiBrowser plugin is released under the terms of the LGPLv3 or higher.
from ...ThingiBrowser.models.ViewOption import ViewOption


class TestViewOption:

    def test_model(self):
        fake_query = lambda: print("Hi!")
        view_option = ViewOption(label="My View", query=fake_query)
        assert view_option.label == "My View"
        assert view_option.query == fake_query
