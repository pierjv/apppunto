from src.models.userModel import userModel
from src.models.serviceModel import serviceModel
from src.entities.serviceEntity import serviceEntity
from src.entities.responseEntity import responseEntity
from src.controllers.responseController import responseController

class serviceController(responseController):

    def get_services(self):
        _message = None
        _status = responseController().interruption
        _data= None
        try:
            _serviceModel = serviceModel()
            _data = _serviceModel.get_services()
            _status = responseController().OK
            _message = responseController().messageOK
        except(Exception) as e:
            _status = responseController().interruption
            _message = responseController().messageInterruption + str(e)
            print('error: '+ str(e))
        return responseEntity(_status,_message,_data).toJSON()
    
    def get_services_by_user(self,index):
        _message = None
        _status = None
        _data= None
        try:
            _serviceModel = serviceModel()
            _data = _serviceModel.get_services_by_user(index)
            _status = self.OK
            _message = self.messageOK
        except(Exception) as e:
            _status = self.interruption
            _message = self.messageInterruption + str(e)
            print('error: '+ str(e))
        return responseEntity(_status,_message,_data).toJSON()
    
    def get_services_load(self):
        _message = None
        _status = None
        _data= None
        try:
            _model = serviceModel()
            _data = _model.get_services_load()
            _status = self.OK
            _message = self.messageOK
        except(Exception) as e:
            _status = self.interruption
            _message = self.messageInterruption + str(e)
            print('error: '+ str(e))
        return responseEntity(_status,_message,_data).toJSON()
        