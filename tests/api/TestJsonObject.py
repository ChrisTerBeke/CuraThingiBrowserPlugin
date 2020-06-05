# Copyright (c) 2020.
# ThingiBrowser plugin is released under the terms of the LGPLv3 or higher.
from ...ThingiBrowser.api.JsonObject import JsonObject, Thing, ApiError, Collection, ThingFile


class TestJsonObject:

    def test_JsonObject_consumes_dict(self):
        json_object = JsonObject({"key": "value"})
        assert json_object.type == "JsonObject"
        assert json_object.toStruct() == {"key": "value", "type": "JsonObject"}

    def test_ApiError(self):
        error = ApiError({"error": "Something horrible has happened"})
        assert error.type == "ApiError"
        assert error.error == "Something horrible has happened"

    def test_Collection(self):
        collection = Collection({
            "description": "My Best Things",
            "id": "12345",
            "name": "Just a Collection",
            "thumbnail": "https://image.com/image",
            "url": "https://things.com/collections/12345",
        })
        assert collection.type == "Collection"
        assert collection.name == "Just a Collection"

    def test_Thing(self):
        thing = Thing({
            "description": "This is not the best Thing in the world, this is just a tribute.",
            "id": "12345",
            "name": "Just a Thing",
            "thumbnail": "https://image.com/image",
            "url": "https://things.com/thingy/12345",
        })
        assert thing.type == "Thing"
        assert thing.name == "Just a Thing"

    def test_ThingFile(self):
        thing_file = ThingFile({
            "id": "12345",
            "name": "thing.stl",
            "thumbnail": "https://image.com/image",
            "url": "https://things.com/thingy/12345/files/12345",
        })
        assert thing_file.type == "ThingFile"
        assert thing_file.name == "thing.stl"
