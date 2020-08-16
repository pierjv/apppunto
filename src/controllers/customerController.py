from src.models.customerModel import customerModel
from src.entities.customerEntity import customerEntity
from src.entities.responseEntity import responseEntity
from src.controllers.responseController import responseController
from src.entities.customeRateEntity import customerRateEntity

class customerController(responseController):

    def get_customers(self):
        _message = None
        _status = responseController().interruption
        return responseEntity(_status,_message,None).toJSON()

    def add_customer(self,request):
        _message = None
        _status = responseController().interruption
        _entity= None
        try:
            _entity = customerEntity()
            _model = customerModel()
            _entity.requestToClass(request)
            _entity = _model.add_customer(_entity)
            _status = responseController().OK
            _message = responseController().messageOK
        except(Exception) as e:
            _status = responseController().interruption
            _message = responseController().messageInterruption +str(e)
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