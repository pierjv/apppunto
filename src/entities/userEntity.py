import json
from collections import namedtuple
 
class userEntity:

    def __init__(self,id=0,mail=None,social_name=None,full_name=None,address=None,document_number=None,type_user=None,photo=None,status=0,password=None):
        self.id = id
        self.mail = mail
        self.social_name = social_name
        self.full_name = full_name
        self.address = address
        self.document_number = document_number
        self.type_user = type_user
        self.photo = photo
        self.status = status
        self.password = password
        
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,sort_keys=True, indent=4)
    
    def requestToClass(self,resquest):
        data = resquest.get_json() 
        print(data)
        print(json.dumps(data))
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
        self.status = 0 
        self.password = values.password