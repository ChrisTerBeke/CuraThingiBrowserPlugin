
class User():
    _user_id = None
    _collections = []

    def __init(self, user_id):
        self.UserID = user_id
        self.Collections = []
        self.retrieveCollections()

    @property
    def UserID(self):
        return self._user_id

    @UserID.setter
    def UserID(self, user_id):
        self._user_id = user_id

    @property
    def Collections(self):
        return self._collections
    
    @Collections.setter
    def Collections(self, collections):
        self.collections = collections

    def retrieveCollections(self):
        