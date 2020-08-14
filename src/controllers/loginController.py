
from src.controllers.responseController import responseController
from src.models.loginModel import loginModel
from src.entities.loginEntity import loginEntity
from src.entities.responseEntity import responseEntity
from src.models.userModel import userModel
from src.entities.userEntity import userEntity

class loginController(responseController):

    def login_user(self,request):
        _message = None
        _status = self.interruption
        _userEntity = None
        try:
            _loginModel = loginModel()
            _loginEntity  = loginEntity()
            _loginEntity.requestToClass(request)
            _userEntity = _loginModel.login_user(_loginEntity)
            if _userEntity is None :
                _status = self.failUser
                _message = self.messageFailUser
            else:
                _status = self.OK
                _message = self.messageOK
        except(Exception) as e:
            _status = self.interruption
            _message = self.messageInterruption + str(e)
            print('error: '+ str(e))
        return responseEntity(_status,_message,_userEntity).toJSON()
    
    def recover_password(self,id):
        _message = None
        _status = self.interruption
        _password = None
        try:
            _model = userModel()
            _entity  = userEntity()
            _password = _model.get_password_by_id(id)
            if _entity is None :
                _status = self.failUser
                _message = self.userDontExist
            else:
                _status = self.OK
                _message = self.messageOK
            print('Enviar SMS con el password: ' + _password)
        except(Exception) as e:
            _status = self.interruption
            _message = self.messageInterruption + str(e)
            print('error: '+ str(e))
        return responseEntity(_status,_message,_password).toJSON()

    def login_customer(self,request):
        _message = None
        _status = self.interruption
        _userEntity = None
        try:
            _loginModel = loginModel()
            _loginEntity  = loginEntity()
            _loginEntity.requestToClass(request)
            _userEntity = _loginModel.login_customer(_loginEntity)
            if _userEntity is None :
                _status = self.failUser
                _message = self.messageFailUser
            else:
                _status = self.OK
                _message = self.messageOK
        except(Exception) as e:
            _status = self.interruption
            _message = self.messageInterruption + str(e)
            print('error: '+ str(e))
        return responseEntity(_status,_message,_userEntity).toJSON()