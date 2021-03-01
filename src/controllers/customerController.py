from src.models.customerModel import customerModel
from src.entities.customerEntity import customerEntity, customerRateEntity,customerCouponEntity, customerAddressEntity , customerCardEntity, customerUserFavoriteEntity
from src.entities.responseEntity import responseEntity
from src.controllers.responseController import responseController
from src.models.chargeModel import chargeModel
import operator

class customerController(responseController):

    def get_customers(self):
        _message = None
        _status = responseController().interruption
        return responseEntity(_status,_message,None).toJSON()

    def add_customer(self,request):
        _message = None
        _status = self.interruption
        _entity= None
        try:
            _entity = customerEntity()
            _model = customerModel()
            _entity.requestToClass(request)
            
            if _model.validate_mail(_entity.mail):
                _status = self.interruption
                _message = self.duplicatedMail
            else:
                if _entity.referred_code == "" or _entity.referred_code is None:
                    _entity = _model.add_customer(_entity)
                    _status = self.OK
                    _message = self.addCustomer  
                else:
                    _id_customer_main = _model.validate_referred_code(_entity.referred_code)
                    if _id_customer_main is not None:
                        _entity = _model.add_customer(_entity)
                        _model.add_customer_coupon(_entity.id,_id_customer_main)
                        _status = self.OK
                        _message = self.addCustomerAndCode
                    else: 
                        _status = self.interruption
                        _message = self.invalidCoupon
                    
        except(Exception) as e:
            _status = self.interruption
            _message = self.messageInterruption +str(e)
            print('error: '+ str(e))
        return responseEntity(_status,_message,_entity).toJSON()

    def update_customer(self,request):
        _message = ''
        _status = self.interruption
        _userEntity= None
        try:
            _customerEntity = customerEntity()
            _customerModel = customerModel()
            _customerEntity.requestUpdateToClass(request)
            _id = _customerModel.update_customer(_customerEntity)
            _status = self.OK
            _message = self.messageOK
        except(Exception) as e:
            _status = self.interruption
            _message = self.messageInterruption +str(e)
            print('error: '+ str(e))
        return responseEntity(_status,_message,_id).toJSON()

    def add_customer_rate(self,request):
        _message = None
        _status = responseController().interruption
        _entity= None
        try:
            _entity = customerRateEntity()
            _model = customerModel()
            _entity.requestToClass(request)
            _entity = _model.add_customer_rate(_entity)
            _status = responseController().OK
            _message = responseController().messageOK
        except(Exception) as e:
            _status = responseController().interruption
            _message = responseController().messageInterruption +str(e)
            print('error: '+ str(e))
        return responseEntity(_status,_message,_entity).toJSON()

    def get_customer_coupon_by_id(self,index):
        _message = None
        _status = self.interruption
        _data= None
        try:
            _model = customerModel()
            _data = _model.get_customer_coupon_by_id(index)
            _status = self.OK
            _message = self.messageOK
        except(Exception) as e:
            _status = self.interruption
            _message = self.messageInterruption + str(e)
            print('error: '+ str(e))
        return responseEntity(_status,_message,_data).toJSON()

    def delete_customer(self,index):
        _message = None
        _status = responseController().interruption
        return responseEntity(_status,_message,None).toJSON()
    

    def get_customer_by_id_(self,index):
        _message = None
        _status = responseController().interruption
        return responseEntity(_status,_message,None).toJSON()
    
    def get_customer_address_by_id_customer(self,index):
        _message = None
        _status = self.interruption
        _data= None
        try:
            _model = customerModel()
            _data = _model.get_customer_address_by_id_customer(index)
            _status = self.OK
            _message = self.messageOK
        except(Exception) as e:
            _status = self.interruption
            _message = self.messageInterruption + str(e)
            print('error: '+ str(e))
        return responseEntity(_status,_message,_data).toJSON()
    
    def get_customer_card_by_id_customer(self,index):
        _message = None
        _status = self.interruption
        _data= None
        try:
            _model = customerModel()
            _data = _model.get_customer_card_by_id_customer(index)
            _status = self.OK
            _message = self.messageOK
        except(Exception) as e:
            _status = self.interruption
            _message = self.messageInterruption + str(e)
            print('error: '+ str(e))
        return responseEntity(_status,_message,_data).toJSON()
    
    def add_customer_address(self,request):
        _message = None
        _status = self.interruption
        _data= None
        try:
            _entity = customerAddressEntity()
            _entity.requestToClass(request)
            _model = customerModel()
            _data = _model.add_customer_address(_entity)
            _status = self.OK
            _message = self.messageOK
        except(Exception) as e:
            _status = self.interruption
            _message = self.messageInterruption + str(e)
            print('error: '+ str(e))
        return responseEntity(_status,_message,_data).toJSON()

    def update_customer_address(self,request):
        _message = None
        _status = self.interruption
        _data= None
        try:
            _entity = customerAddressEntity()
            _entity.requestToClassUpdate(request)
            _model = customerModel()
            _data = _model.update_customer_address(_entity)
            _status = self.OK
            _message = self.messageOK
        except(Exception) as e:
            _status = self.interruption
            _message = self.messageInterruption + str(e)
            print('error: '+ str(e))
        return responseEntity(_status,_message,_data).toJSON()
    
    def delete_customer_address(self,index):
        _message = None
        _status = self.interruption
        id_customer_address= None
        try:
            _model = customerModel()
            id_customer_address = _model.delete_customer_address(index)
            _status = self.OK
            _message = self.messageOK
        except(Exception) as e:
            _status = self.interruption
            _message = self.messageInterruption + str(e)
            print('error: '+ str(e))
        return responseEntity(_status,_message,id_customer_address).toJSON()

    def add_customer_card(self,request):
        _message = None
        _status = self.interruption
        _data_card= None
        _data = None
        try:
            _entity = customerCardEntity()
            _entity.requestToClass(request)
            _model = customerModel()
            _chargeModel = chargeModel()
            _data = _chargeModel.add_card_culqi(_entity.cvv,_entity.cardNumberNotEncrypted,_entity.expYearNotEncripted,_entity.expMonthNotEcrypted,_entity.email)
            
            if _data["object"] == "error":
                _status = self.interruption
                _message = _data["user_message"]
            else:
                _data_card = _model.add_customer_card(_entity)
                _status = self.OK
                _message = self.messageOK
        except(Exception) as e:
            _status = self.interruption
            _message = self.messageInterruption + str(e)
            print('error: '+ str(e))
        return responseEntity(_status,_message,_data_card).toJSON()
    
    def delete_customer_card(self,index):
        _message = None
        _status = self.interruption
        id_customer_address= None
        try:
            _model = customerModel()
            id_customer_address = _model.delete_customer_card(index)
            _status = self.OK
            _message = self.messageOK
        except(Exception) as e:
            _status = self.interruption
            _message = self.messageInterruption + str(e)
            print('error: '+ str(e))
        return responseEntity(_status,_message,id_customer_address).toJSON()
    
    def update_customer_user_favorite(self,request):
        _message = None
        _status = self.interruption
        try:
            _entity = customerUserFavoriteEntity()
            _entity.requestToClass(request)
            _model = customerModel()
            _entity = _model.update_customer_user_favorite(_entity)
            _status = self.OK
            _message = self.messageOK
        except(Exception) as e:
            _status = self.interruption
            _message = self.messageInterruption + str(e)
            print('error: '+ str(e))
        return responseEntity(_status,_message,_entity).toJSON()