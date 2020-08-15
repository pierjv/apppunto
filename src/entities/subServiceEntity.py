import json
from collections import namedtuple
from src.entities.userStoreEntity import userStoreEntity
 
class subServiceEntity:

    def __init__(self,id= None, full_name = None,charge = None, enable = None):
        self.id = id
        self.full_name = full_name
        self.charge = charge
        self.enable = enable

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,sort_keys=True, indent=4)
        