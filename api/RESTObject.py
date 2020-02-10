import abc
from abc import ABC, abstractmethod

class RESTObject():

    @abstractmethod
    def _executeQuery(self, query: Optional[str] = None) -> None:
        """
        Internal function to query the API for things.
        :param new_query: Perform a new query instead of adding a new page to the existing one.
        :param is_from_collection: Specifies whether the resulting Things are part of a collection or not
        """
        if new_query:
            self._query = new_query
            self._clearSearchResults()
            self._query_page = 1
        if self._is_from_collection != is_from_collection:
            self._is_from_collection = is_from_collection
            self.isFromCollectionChanged.emit()
        self._is_querying = True
        self.queryingStateChanged.emit()
        self._api_client.get(self._query, page=self._query_page, on_finished=self._onQueryFinished,
                             on_failed=self._onRequestFailed)