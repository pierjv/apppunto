import json
from collections import namedtuple
from src.entities.userStoreEntity import userStoreEntity
 
class loginEntity:

    def __init__(self,mail= None, password = None):
        self.mail = mail
        self.password = password

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,sort_keys=True, indent=4)
    
    def requestToClass(self,resquest):
        data = resquest.get_json() 
        data = json.dumps(data)
        values = json.loads(data, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
        self.mail = values.mail
        self.password = values.password