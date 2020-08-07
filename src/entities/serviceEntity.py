import json
from collections import namedtuple
from src.entities.userStoreEntity import userStoreEntity
 
class serviceEntity:

    def __init__(self,id= None, full_name = None, url_image = None, enable = None,status = None):
        self.id = id
        self.full_name = full_name
        self.url_image = url_image
        self.enable  = enable
        self.status = status

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,sort_keys=True, indent=4)
        