import json
from collections import namedtuple

class customerRateEntity:

    def __init__(self,id_user=0,id_service=None,id_customer=None,rate=None,description=None):
        self.id_user = id_user
        self.id_service = id_service
        self.id_customer = id_customer
        self.rate = rate
        self.description = description
        
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,sort_keys=True, indent=4)
    
    def requestToClass(self,resquest):
        data = resquest.get_json() 
        data = json.dumps(data)
        values = json.loads(data, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
        self.id_user = values.id_user
        self.id_service = values.id_service 
        self.id_customer = values.id_customer
        self.rate = values.rate
        self.description = values.description