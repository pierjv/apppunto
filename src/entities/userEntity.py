import json
from collections import namedtuple
from src.entities.userStoreEntity import userStoreEntity
 
class userEntity:

    def __init__(self,id=0,mail=None,social_name=None,full_name=None,
                document_number=None,type_user=None,photo=None,password=None,
                cellphone=None,about=None,id_type_document = None,user_store= None,
                avg_rate=None):
        self.id = id
        self.mail = mail
        self.social_name = social_name
        self.full_name = full_name
        self.document_number = document_number
        self.type_user = type_user
        self.photo = photo
        self.cellphone = cellphone
        self.about = about
        self.password = password
        self.id_type_document = id_type_document
        self.user_store = user_store
        self.avg_rate = avg_rate

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
        self.document_number = values.document_number
        self.type_user = values.type_user
        self.photo = values.photo
        self.cellphone = values.cellphone
        self.about = values.about
        self.id_type_document = values.id_type_document
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
    

    def requestUpdateToClass(self,resquest):
        data = resquest.get_json() 
        data = json.dumps(data)
        values = json.loads(data, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
        self.id = values.id
        self.social_name = values.social_name
        self.full_name = values.full_name
        self.id_type_document = values.id_type_document
        self.document_number = values.document_number
        self.photo = values.photo
        self.cellphone = values.cellphone
        self.about = values.about

    def requestToEmail(self,resquest):
        data = resquest.get_json() 
        data = json.dumps(data)
        values = json.loads(data, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
        self.mail = values.mail
    
    def requestSubServiceToString(self,request):
        data = request.get_json() 
        data = json.dumps(data)
        values = json.loads(data, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
        _subs_services = ""
        _len = len(values.sub_services)
        _i = 1
        for us in values.sub_services:
            _subs_services += str(us) 
            if _i < _len:
                _subs_services += ","
            _i = _i + 1
            
        return _subs_services

class userSubServiceFilterEntity:

    def __init__(self,type_user=None,sub_services = None):
        self.type_user = type_user
        self.sub_services = sub_services
    
    def requestToClass(self,request):
        data = request.get_json() 
        data = json.dumps(data)
        values = json.loads(data, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
        _subs_services = ""
        _len = len(values.sub_services)
        _i = 1
        for us in values.sub_services:
            _subs_services += str(us) 
            if _i < _len:
                _subs_services += ","
            _i = _i + 1
        self.sub_services = _subs_services
        self.type_user = values.type_user
        
            

class userServiceEntity:

    def __init__(self,id_service=None,service_full_name = None, users= None):
        self.id_service = id_service
        self.service_full_name = service_full_name
        self.users = users

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,sort_keys=True, indent=4)

class userServiceAddEntity:
    def __init__(self,id_service=None,id_user = None, enable= None):
        self.id_service = id_service
        self.id_user = id_user
        self.enable = enable

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,sort_keys=True, indent=4)

class lstuserServiceAddEntity:
    def __init__(self,user_services=None):
        self.user_services = user_services

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,sort_keys=True, indent=4)

    def requestToClass(self,resquest):
        data = resquest.get_json() 
        data = json.dumps(data)
        values = json.loads(data, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
        _user_services =[]
        for us in values:
            _entity = userServiceAddEntity()
            _entity.id_service = us.id_service
            _entity.id_user = us.id_user
            _entity.enable = us.enable
            _user_services.append(_entity)
        self.user_services = _user_services 


class typeDocumentEntity:

    def __init__(self,id=None,full_name= None):
        self.id = id
        self.full_name = full_name

class bankEntity:

    def __init__(self,id=None,full_name= None):
        self.id = id
        self.full_name = full_name

class rateEntity:

    def __init__(self,rate=None,total=None,quantity=None,percentage=None):
        self.rate = rate
        self.total = total
        self.quantity = quantity
        self.percentage = percentage
        
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,sort_keys=True, indent=4)

class commentEntity:

    def __init__(self,rate=None,description=None,date_transaction=None,full_name=None):
        self.rate = rate
        self.description = description
        self.date_transaction = date_transaction
        self.full_name = full_name
        
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,sort_keys=True, indent=4)

class userDetailEntity:

    def __init__(self,services=None,rates=None,comments=None, flag_favorite=None):
        self.services = services
        self.rates = rates
        self.comments = comments
        self.flag_favorite = flag_favorite
        
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,sort_keys=True, indent=4)
    
class dashboardEntity:

    def __init__(self,users=0,customers=0,total_amount=0,sales=0,average_amount=0,
                max_hour_availability=0,sales_per_day=0,amount_per_day= 0):
        self.users = users
        self.customers = customers
        self.total_amount = total_amount
        self.sales = sales
        self.average_amount = average_amount
        self.max_hour_availability = max_hour_availability
        self.sales_per_day = sales_per_day
        self.amount_per_day = amount_per_day
    
    def classToFormat(self):
        self.users = "{:d}".format(self.users)
        self.customers = "{:d}".format(self.customers)
        self.total_amount = "S/. "+"{:8.1f}".format(self.total_amount)
        self.sales = "{:d}".format(self.sales)
        self.max_hour_availability = str(self.max_hour_availability) + ":00 h"
        self.average_amount = "S/. "+"{:8.1f}".format(self.average_amount)
        self.sales_per_day = "{:8.1f}".format(self.sales_per_day)
        self.amount_per_day = "S/. "+"{:8.1f}".format(self.amount_per_day)

class dashboardServiceEntity:

    def __init__(self,id_service=None,service=None,users=None,amount=None,sales=None,
                average_sale=None,max_hour_availability=None,sales_q_1= None,sales_q_2 = None,
                sales_q_3=None,sales_q_4=None,sales_q_5= None,sales_q_6 = None,sales_q_7 = None,
                sales_a_1=None,sales_a_2=None,sales_a_3= None,sales_a_4 = None,sales_a_5 = None,
                sales_a_6=None,sales_a_7=None):
        self.id_service = id_service
        self.service = service
        self.users = users
        self.amount = amount
        self.sales = sales
        self.average_sale = average_sale
        self.max_hour_availability = max_hour_availability
        self.sales_q_1 = sales_q_1
        self.sales_q_2 = sales_q_2
        self.sales_q_3 = sales_q_3
        self.sales_q_4 = sales_q_4
        self.sales_q_5 = sales_q_5
        self.sales_q_6 = sales_q_6
        self.sales_q_7 = sales_q_7
        self.sales_a_1 = sales_a_1
        self.sales_a_2 = sales_a_2
        self.sales_a_3 = sales_a_3
        self.sales_a_4 = sales_a_4
        self.sales_a_5 = sales_a_5
        self.sales_a_6 = sales_a_6
        self.sales_a_7 = sales_a_7

    def valueToCero(self,value):
        if(value is None):
            value = 0
        return value
    
    def valuesToFormat(self):
        self.id_service = self.valueToCero(self.id_service)
        self.service = self.valueToCero(self.service)
        self.users = self.valueToCero(self.users)
        self.amount = self.valueToCero(self.amount)
        self.sales = self.valueToCero(self.sales)
        self.average_sale = self.valueToCero(self.average_sale)
        self.max_hour_availability = self.valueToCero(self.max_hour_availability)
        self.sales_q_1 = self.valueToCero(self.sales_q_1)
        self.sales_q_2 = self.valueToCero(self.sales_q_2)
        self.sales_q_3 = self.valueToCero(self.sales_q_3)
        self.sales_q_4 = self.valueToCero(self.sales_q_4)
        self.sales_q_5 = self.valueToCero(self.sales_q_5)
        self.sales_q_6 = self.valueToCero(self.sales_q_6)
        self.sales_q_7 = self.valueToCero(self.sales_q_7)
        self.sales_a_1 = self.valueToCero(self.sales_a_1)
        self.sales_a_2 = self.valueToCero(self.sales_a_2)
        self.sales_a_3 = self.valueToCero(self.sales_a_3)
        self.sales_a_4 = self.valueToCero(self.sales_a_4)
        self.sales_a_5 = self.valueToCero(self.sales_a_5)
        self.sales_a_6 = self.valueToCero(self.sales_a_6)
        self.sales_a_7 = self.valueToCero(self.sales_a_7)

    def classToFormat(self):
        self.users = "{:d}".format(self.users)
        self.amount = "S/. "+"{:8.1f}".format(self.amount)
        self.sales = "{:d}".format(self.sales)
        self.average_sale = "S/. "+"{:8.1f}".format(self.average_sale)
        self.max_hour_availability = str(self.max_hour_availability) + ":00 h"
        self.sales_q_1 = "{:8.1f}".format(self.sales_q_1)
        self.sales_q_2 = "{:8.1f}".format(self.sales_q_2)
        self.sales_q_3 = "{:8.1f}".format(self.sales_q_3)
        self.sales_q_4 = "{:8.1f}".format(self.sales_q_4)
        self.sales_q_5 = "{:8.1f}".format(self.sales_q_5)
        self.sales_q_6 = "{:8.1f}".format(self.sales_q_6)
        self.sales_q_7 = "{:8.1f}".format(self.sales_q_7)
        self.sales_a_1 = "S/. "+"{:8.1f}".format(self.sales_a_1)
        self.sales_a_2 = "S/. "+"{:8.1f}".format(self.sales_a_2)
        self.sales_a_3 = "S/. "+"{:8.1f}".format(self.sales_a_3)
        self.sales_a_4 = "S/. "+"{:8.1f}".format(self.sales_a_4)
        self.sales_a_5 = "S/. "+"{:8.1f}".format(self.sales_a_5)
        self.sales_a_6 = "S/. "+"{:8.1f}".format(self.sales_a_6)
        self.sales_a_7 = "S/. "+"{:8.1f}".format(self.sales_a_7)


class userMobileDashboardEntity:

    def __init__(self,id=None,full_name=None,value=None):
        self.id = id
        self.full_name = full_name
        self.value = value
        
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,sort_keys=True, indent=4)

class userSubServiceAddEntity:

    def __init__(self,id_user=None,id_service=None,id_sub_service=None,charge = None,enable = None):
        self.id_user = id_user
        self.id_service = id_service
        self.id_sub_service = id_sub_service
        self.charge = charge
        self.enable = enable
        
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,sort_keys=True, indent=4)

class lstUserSubServiceAddEntity:
    def __init__(self,user_sub_services=None):
        self.user_sub_services = user_sub_services

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,sort_keys=True, indent=4)

    def requestToClass(self,resquest):
        data = resquest.get_json() 
        data = json.dumps(data)
        values = json.loads(data, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
        _user_sub_services =[]
        for us in values:
            _entity = userSubServiceAddEntity()
            _entity.id_user = us.id_user
            _entity.id_service = us.id_service
            _entity.id_sub_service = us.id_sub_service
            _entity.charge = us.charge
            _entity.enable = us.enable
            _user_sub_services.append(_entity)
        self.user_sub_services = _user_sub_services 

class userBankEntity:

    def __init__(self,id=None,id_user = None, id_bank= None, account_number = None, cci= None):
        self.id = id
        self.id_user = id_user
        self.id_bank = id_bank
        self.account_number = account_number
        self.cci = cci
        
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,sort_keys=True, indent=4)

    def requestToClass(self,resquest):
        data = resquest.get_json() 
        data = json.dumps(data)
        values = json.loads(data, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
        self.id_user = values.id_user
        self.id_bank = values.id_bank
        self.account_number = values.account_number
        self.cci = values.cci
    
    def requestUpdateToClass(self,resquest):
        data = resquest.get_json() 
        data = json.dumps(data)
        values = json.loads(data, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
        self.id = values.id
        self.id_user = values.id_user
        self.id_bank = values.id_bank
        self.account_number = values.account_number
        self.cci = values.cci