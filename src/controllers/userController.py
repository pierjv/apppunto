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
        _userEntity= None
        try:
            _userEntity = userEntity()
            _userModel = userModel()
            _userEntity.requestToClass(request)
            _userEntity = _userModel.add_user(_userEntity)
            _status = responseController().OK
            _message = responseController().messageOK
        except(Exception) as e:
            _status = responseController().interruption
            _message = responseController().messageInterruption +str(e)
            print('error: '+ str(e))
        return responseEntity(_status,_message,_userEntity).toJSON()

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