from src.models.userModel import userModel
from src.entities.userEntity import userEntity
from src.entities.responseEntity import responseEntity
from src.controllers.responseController import responseController

class userController(responseController):

    def get_users(self):
        _message = None
        _status = responseController().interruption
        _data= None
        try:
            _userEntity = userEntity()
            _userModel = userModel()
            _data = _userModel.get_users()
            _status = responseController().OK
            _message = responseController().messageOK
        except(Exception) as e:
            _status = responseController().interruption
            _message = responseController().messageInterruption + str(e)
            print('error: '+ str(e))
        return responseEntity(_status,_message,_data).toJSON()

    def add_user(self,request):
        _message = None
        _status = responseController().interruption
        _entity= None
        try:
            _entity = userEntity()
            _model = userModel()
            _entity.requestToClass(request)
            if _model.validate_mail(_entity.mail):
                _status = responseController().interruption
                _message = responseController().duplicatedMail
            else:
                _entity = _model.add_user(_entity)
                _status = responseController().OK
                _message = responseController().messageOK
        except(Exception) as e:
            _status = responseController().interruption
            _message = responseController().messageInterruption +str(e)
            print('error: '+ str(e))
        return responseEntity(_status,_message,_entity).toJSON()

    def delete_user(self,index):
        _message = None
        _status = responseController().interruption
        _userEntity= None
        try:
            _userModel = userModel()
            _userEntity = userEntity()
            _id = _userModel.delete_user(index)
            _userEntity.id = _id
            _status = responseController().OK
            _message = responseController().messageOK 
        except(Exception) as e:
            _status = responseController().interruption
            _message = responseController().messageInterruption +str(e)
            print('error: '+ str(e))    
        return responseEntity(_status,_message,_userEntity).toJSON()
    
    def update_user(self,request,index):
        _message = ''
        _status = responseController().interruption
        _userEntity= None
        try:
            _userEntity = userEntity()
            _userModel = userModel()
            _userEntity.requestToClass(request)
            _userEntity.id = index
            _id = _userModel.update_user(_userEntity)
            _status = responseController().OK
            _message = responseController().messageOK
        except(Exception) as e:
            _status = responseController().interruption
            _message = responseController().messageInterruption +str(e)
            print('error: '+ str(e))
        return responseEntity(_status,_message,_userEntity).toJSON()

    def get_user_by_id_service(self,index):
        _message = None
        _status = self.interruption
        _data = None
        try:
            _model = userModel()
            _data = _model.get_user_by_id_service(index)
            if _data is None or len(_data) < 1:
                _status = self.OK
                _message = self.dontExistValues
            else:
                _status = self.OK
                _message = self.messageOK
        except(Exception) as e:
            _status = self.interruption
            _message = self.messageInterruption +str(e)
            print('error: '+ str(e))
        return responseEntity(_status,_message,_data).toJSON()
    
    def get_user_detail(self,index):
        _message = None
        _status = None
        _data= None
        try:
            _model = userModel()
            _data = _model.get_user_detail(index)
            _status = self.OK
            _message = self.messageOK
        except(Exception) as e:
            _status = self.interruption
            _message = self.messageInterruption + str(e)
            print('error: '+ str(e))
        return responseEntity(_status,_message,_data).toJSON()