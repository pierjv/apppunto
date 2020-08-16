import json
from collections import namedtuple
from src.entities.userStoreEntity import userStoreEntity
 
class customerAddressEntity:

    def __init__(self,id=0,id_customer=None,address=None,longitude=None,latitude=None,
                main=None):
        self.id = id
        self.id_customer = id_customer
        self.address = address
        self.longitude = longitude
        self.latitude = latitude
        self.main = main

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,sort_keys=True, indent=4)
    