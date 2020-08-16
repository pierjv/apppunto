import json
from collections import namedtuple
from src.entities.customerAddressEntity import customerAddressEntity
 
class customerEntity:

    def __init__(self,id=0,mail=None,full_name=None,cellphone=None,photo=None,
                password=None,customer_address= None):
        self.id = id
        self.mail = mail
        self.full_name = full_name
        self.cellphone = cellphone
        self.photo = photo
        self.password = password
        self.customer_address = customer_address

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,sort_keys=True, indent=4)
    
    def requestToClass(self,resquest):
        data = resquest.get_json() 
        data = json.dumps(data)
        values = json.loads(data, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
        self.id = values.id
        self.mail = values.mail
        self.full_name = values.full_name
        self.cellphone = values.cellphone
        self.photo = values.photo
        self.password = values.password
        _customer_address =[]
        for us in values.customer_address:
            _entity = customerAddressEntity()
            _entity.id_customer = us.id_customer
            _entity.address = us.address
            _entity.longitude = us.longitude
            _entity.latitude = us.latitude
            _entity.main = us.main
            _customer_address.append(_entity)
        self.customer_address = _customer_address 