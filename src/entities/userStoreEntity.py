import json
from collections import namedtuple
 
class userStoreEntity:

    def __init__(self,id=0,mail=None,id_user=None,full_name=None,address=None,
                longitude=None,latitude=None,main=None):
        self.id = id
        self.id_user = id_user 
        self.full_name = full_name
        self.address = address
        self.longitude = longitude
        self.latitude = latitude
        self.main = main

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,sort_keys=True, indent=4)
    
    def requestToClass(self,resquest):
        data = resquest.get_json() 
        data = json.dumps(data)
        values = json.loads(data, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
        self.id_user = values.id_user 
        self.full_name = values.full_name
        self.address = values.address
        self.longitude = values.longitude
        self.latitude = values.latitude
        self.main = values.main

        