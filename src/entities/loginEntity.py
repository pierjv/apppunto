import json
from collections import namedtuple
from src.entities.userStoreEntity import userStoreEntity
import yaml as yml

class loginEntity:

    def __init__(self,mail= None, password = None, id_fire_base_token = None):
        self.mail = mail
        self.password = password
        self.id_fire_base_token = id_fire_base_token

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,sort_keys=True, indent=4)
    
    def requestToClass(self,resquest):
        data = resquest.get_json() 
        data = json.dumps(data)
        values = json.loads(data, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
        self.mail = values.mail
        self.password = values.password
        self.id_fire_base_token = values.id_fire_base_token

class tokenEntity:
    def __init__(self):
        with open('src/cn/.env.yml') as f:
            env_vars = yml.full_load(stream=f)
        self.user = env_vars['Tk_USER']
        self.password = env_vars['TK_PASW']

    def validate_request(self,resquest):
        data = resquest.get_json() 
        data = json.dumps(data)
        values = json.loads(data, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
        _value = False
        if self.user == values.user and self.password == values.password:
            _value = True
        return _value

class loadEntity:

    def __init__(self,services= None, type_documents = None,preferred_users= None , delivery_costs = None, banks = None):
        self.services = services
        self.type_documents = type_documents
        self.preferred_users = preferred_users
        self.delivery_costs = delivery_costs
        self.banks = banks

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,sort_keys=True, indent=4)
