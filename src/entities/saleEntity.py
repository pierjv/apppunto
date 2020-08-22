import json
from collections import namedtuple
 
class saleEntity:

    def __init__(self,id=0,id_type_availability=None,id_customer=None,id_user=None,coupon=None,
                date_availability=None,hour_availability= None,total_amount= None,id_type_card = None,
                document_number=None,expiration_year =None,expiration_month=None,mail=None,
                full_name_card=None, type_sales = None):
        self.id = id
        self.id_type_availability = id_type_availability
        self.id_customer = id_customer
        self.id_user = id_user
        self.coupon = coupon
        self.date_availability = date_availability
        self.hour_availability = hour_availability
        self.total_amount = total_amount
        self.id_type_card = id_type_card
        self.document_number = document_number
        self.expiration_year = expiration_year
        self.expiration_month = expiration_month
        self.mail = mail
        self.full_name_card = full_name_card
        self.type_sales = type_sales

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,sort_keys=True, indent=4)
    
    def requestToClass(self,resquest):
        data = resquest.get_json() 
        data = json.dumps(data)
        values = json.loads(data, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
        self.id_type_availability = values.id_type_availability
        self.id_customer = values.id_customer
        self.id_user = values.id_user
        self.coupon = values.coupon
        self.date_availability = values.date_availability
        self.hour_availability = values.hour_availability
        self.total_amount = values.total_amount
        self.id_type_card = values.id_type_card
        self.document_number = values.document_number
        self.expiration_year = values.expiration_year
        self.expiration_month = values.expiration_month
        self.mail = values.mail
        self.full_name_card = values.full_name_card

        _type_sales =[]

        for us in values.type_sales:
            _entity = typeSaleEntity()
            _entity.id_sub_service = us.id_sub_service
            _entity.amount = us.amount
            _type_sales.append(_entity)
        self.type_sales = _type_sales 
        
    def requestToEmail(self,resquest):
        data = resquest.get_json() 
        data = json.dumps(data)
        values = json.loads(data, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
        self.mail = values.mail

class typeSaleEntity:

    def __init__(self,id=0,id_sale=None,id_sub_service=None,amount=None):
        self.id = id
        self.id_sale = id_sale
        self.id_sub_service = id_sub_service
        self.amount = amount

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,sort_keys=True, indent=4)