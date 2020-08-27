import json
from collections import namedtuple
 
class customerEntity:

    def __init__(self,id=0,mail=None,full_name=None,cellphone=None,photo=None,
                password=None,id_code = None,referred_code = None,customer_address= None):
        self.id = id
        self.mail = mail
        self.full_name = full_name
        self.cellphone = cellphone
        self.photo = photo
        self.password = password
        self.id_code = id_code
        self.referred_code = referred_code
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
        self.referred_code = values.referred_code
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
        
    def requestToEmail(self,resquest):
        data = resquest.get_json() 
        data = json.dumps(data)
        values = json.loads(data, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
        self.mail = values.mail

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

class customerCouponEntity:

    def __init__(self,id=0,coupon=None,id_customer=None,effective_date=None):
        self.id = id
        self.coupon = coupon
        self.id_customer = id_customer
        self.effective_date = effective_date
        
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,sort_keys=True, indent=4)