import json
from collections import namedtuple
 
class saleEntity:

    def __init__(self,id=0,id_type_availability=None,id_customer=None,id_user=None,coupon=None,
                date_availability=None,hour_availability= None,total_amount= None,id_type_card = None,
                document_number=None,expiration_year =None,expiration_month=None,mail=None,
                full_name_card=None,id_customer_address = None, type_sales = None,amount_coupon = None,
                id_user_store = None,amount_delivery=None,comment = None):
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
        self.id_customer_address = id_customer_address
        self.type_sales = type_sales
        self.amount_coupon = amount_coupon
        self.id_user_store = id_user_store
        self.amount_delivery = amount_delivery
        self.comment =comment

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
        self.id_customer_address = values.id_customer_address
        self.amount_coupon = values.amount_coupon
        self.id_user_store = values.id_user_store
        self.amount_delivery = values.amount_delivery
        self.comment = values.comment

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

class saleResponseEntity:

    def __init__(self,id=0,id_type_availability=None,full_name_type_availability=None,id_customer=None,id_user=None,coupon=None,
                date_availability=None,hour_availability= None,total_amount= None,id_type_card = None,
                document_number=None,expiration_year =None,expiration_month=None,mail=None,full_name_card=None, status_sale= None,
                id_customer_address = None,address = None, type_sales = None, full_name_customer = None, url_image_customer = None):
        self.id = id
        self.id_type_availability = id_type_availability
        self.full_name_type_availability = full_name_type_availability
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
        self.status_sale = status_sale
        self.id_customer_address = id_customer_address
        self.address = address
        self.type_sales = type_sales
        self.full_name_customer = full_name_customer
        self.url_image_customer = url_image_customer

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,sort_keys=True, indent=4)

class saleConfirmEntity:

    def __init__(self,id_sale=None,total_amount= None,
                document_number=None,expiration_year =None,expiration_month=None,mail=None,
                full_name_card=None, cvv = None):
        self.id_sale = id_sale
        self.total_amount = total_amount
        self.document_number = document_number
        self.expiration_year = expiration_year
        self.expiration_month = expiration_month
        self.mail = mail
        self.full_name_card = full_name_card
        self.cvv = cvv

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,sort_keys=True, indent=4)

    def requestToClass(self,resquest):
        data = resquest.get_json() 
        data = json.dumps(data)
        values = json.loads(data, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
        self.id_sale = values.id_sale
        self.total_amount = values.total_amount
        self.document_number = values.document_number
        self.expiration_year = values.expiration_year
        self.expiration_month = values.expiration_month
        self.mail = values.mail
        self.full_name_card = values.full_name_card
        self.cvv = values.cvv



class typeSaleEntity:

    def __init__(self,id=0,id_sale=None,id_sub_service=None,amount=None):
        self.id = id
        self.id_sale = id_sale
        self.id_sub_service = id_sub_service
        self.amount = amount

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,sort_keys=True, indent=4)


class typeSaleResponseEntity:

    def __init__(self,id=0,id_sale=None,id_sub_service=None,amount=None,full_name= None):
        self.id = id
        self.id_sale = id_sale
        self.id_sub_service = id_sub_service
        self.amount = amount
        self.full_name = full_name

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,sort_keys=True, indent=4)

class deliveryCost:
    def __init__(self,from_km=0,to_km=None,fixed_cost=None,delivery=None):
        self.from_km = from_km
        self.to_km = to_km
        self.fixed_cost = fixed_cost
        self.delivery = delivery

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,sort_keys=True, indent=4)
