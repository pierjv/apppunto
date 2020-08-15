import json
from collections import namedtuple
from src.entities.userStoreEntity import userStoreEntity
 
class userEntity:

    def __init__(self,id=0,mail=None,social_name=None,full_name=None,address=None,
                document_number=None,type_user=None,photo=None,status=None,password=None,
                cellphone=None,about=None,user_store= None,service = None):
        self.id = id
        self.mail = mail
        self.social_name = social_name
        self.full_name = full_name
        self.address = address
        self.document_number = document_number
        self.type_user = type_user
        self.photo = photo
        self.cellphone = cellphone
        self.about = about
        self.password = password
        self.user_store = user_store

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,sort_keys=True, indent=4)
    
    def requestToClass(self,resquest):
        data = resquest.get_json() 
        data = json.dumps(data)
        values = json.loads(data, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
        self.id = values.id
        self.mail = values.mail
        self.social_name = values.social_name
        self.full_name = values.full_name
        self.address = values.address
        self.document_number = values.document_number
        self.type_user = values.type_user
        self.photo = values.photo
        self.cellphone = values.cellphone
        self.about = values.about
        self.password = values.password
        _user_store =[]
        for us in values.user_store:
            _userStoreEntity = userStoreEntity()
            _userStoreEntity.id_user = us.id_user
            _userStoreEntity.full_name = us.full_name
            _userStoreEntity.address = us.address
            _userStoreEntity.longitude = us.longitude
            _userStoreEntity.latitude = us.latitude
            _userStoreEntity.main = us.main
            _user_store.append(_userStoreEntity)
        self.user_store = _user_store 

class typeDocumentEntity:

    def __init__(self,id=None,full_name= None):
        self.id = id
        self.full_name = full_name
        