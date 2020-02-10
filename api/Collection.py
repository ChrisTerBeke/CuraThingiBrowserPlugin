from ..thingiverse.ThingiverseApiClient import ThingiverseApiClient

class Collection():
    _things = []

    def __init__(self):
        self._things = []

    @staticmethod
    def search(collection_name = None, user_name = None):
        ThingiverseApiClient.get('/')