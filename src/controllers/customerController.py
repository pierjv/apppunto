from src.models.customerModel import customerModel
from src.entities.customerEntity import customerEntity, customerRateEntity
from src.entities.responseEntity import responseEntity
from src.controllers.responseController import responseController
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
                if _entity.referred_coupon != "" and _entity.referred_coupon is not None and operator.not_(_model.validate_referred_coupon(_entity.referred_coupon)):
                    _status = self.interruption
                    _message = self.invalidCoupon
                else:
                    _entity = _model.add_customer(_entity)
                    _status = self.OK
                    _message = self.messageOK
        except(Exception) as e:
            _status = self.interruption
            _message = self.messageInterruption +str(e)
            print('error: '+ str(e))
        return responseEntity(_status,_message,_entity).toJSON()

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

    def delete_customer(self,index):
        _message = None
        _status = responseController().interruption
        return responseEntity(_status,_message,None).toJSON()
    
    def update_customer(self,request,index):
        _message = None
        _status = responseController().interruption
        return responseEntity(_status,_message,None).toJSON()

    def get_customer_by_id_(self,index):
        _message = None
        _status = responseController().interruption
        return responseEntity(_status,_message,None).toJSON()