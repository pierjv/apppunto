import json
from collections import namedtuple
from src.entities.userStoreEntity import userStoreEntity
 
class serviceEntity:

    def __init__(self,id= None, full_name = None, url_image = None, enable = None,sub_services= None, color = None,file_image = None):
        self.id = id
        self.full_name = full_name
        self.enable  = enable
        self.sub_services = sub_services
        self.color = color
        self.file_image = file_image

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,sort_keys=True, indent=4)


class serviceUserEntity:
    def __init__(self,id_user= None, id_service = None):
        self.id_user = id_user
        self.id_service = id_service
    
    def requestToClass(self,resquest):
        data = resquest.get_json() 
        data = json.dumps(data)
        values = json.loads(data, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
        self.id_user = values.id_user
        self.id_service = values.id_service

        