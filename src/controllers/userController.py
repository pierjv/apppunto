from src.models.userModel import userModel
from src.entities.userEntity import userEntity
from src.entities.responseEntity import responseEntity
from src.controllers.responseController import responseController

class userController(responseController):

    def get_users(self):
        _message = None
        _status = self.interruption
        _data= None
        try:
            _userEntity = userEntity()
            _userModel = userModel()
            _data = _userModel.get_users()
            _status = self.OK
            _message = self.messageOK
        except(Exception) as e:
            _status = self.interruption
            _message = self.messageInterruption + str(e)
            print('error: '+ str(e))
        return responseEntity(_status,_message,_data).toJSON()

    def add_user(self,request):
        _message = None
        _status = self.interruption
        _entity= None
        try:
            _entity = userEntity()
            _model = userModel()
            _entity.requestToClass(request)
            if _model.validate_mail(_entity.mail):
                _status = self.interruption
                _message = self.duplicatedMail
            else:
                _entity = _model.add_user(_entity)
                _status = self.OK
                _message = self.messageOK
        except(Exception) as e:
            _status = self.interruption
            _message = self.messageInterruption +str(e)
            print('error: '+ str(e))
        return responseEntity(_status,_message,_entity).toJSON()

    def delete_user(self,index):
        _message = None
        _status = self.interruption
        _userEntity= None
        try:
            _userModel = userModel()
            _userEntity = userEntity()
            _id = _userModel.delete_user(index)
            _userEntity.id = _id
            _status = self.OK
            _message = self.messageOK 
        except(Exception) as e:
            _status = self.interruption
            _message = self.messageInterruption +str(e)
            print('error: '+ str(e))    
        return responseEntity(_status,_message,_userEntity).toJSON()
    
    def update_user(self,request,index):
        _message = ''
        _status = self.interruption
        _userEntity= None
        try:
            _userEntity = userEntity()
            _userModel = userModel()
            _userEntity.requestToClass(request)
            _userEntity.id = index
            _id = _userModel.update_user(_userEntity)
            _status = self.OK
            _message = self.messageOK
        except(Exception) as e:
            _status = self.interruption
            _message = self.messageInterruption +str(e)
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

    def get_dashboard_general(self):
        _entity= None
        try:
            _userModel = userModel()
            _entity = _userModel.get_dashboard_general()
        except(Exception) as e:
            print('error: '+ str(e))
        return _entity
    
    def get_dashboard_service(self):
        _data= None
        try:
            _userModel = userModel()
            _data = _userModel.get_dashboard_service()
        except(Exception) as e:
            print('error: '+ str(e))
        return _data