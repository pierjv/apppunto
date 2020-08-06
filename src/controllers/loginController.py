
from src.controllers.responseController import responseController
from src.models.loginModel import loginModel
from src.entities.loginEntity import loginEntity
from src.entities.responseEntity import responseEntity

class loginController(responseController):

    def login_user(self,request):
        _message = None
        _status = responseController().interruption
        _userEntity = None
        try:
            _loginModel = loginModel()
            _loginEntity  = loginEntity()
            _loginEntity.requestToClass(request)
            _userEntity = _loginModel.login_user(_loginEntity)
            if _userEntity is None :
                _status = responseController().failUser
                _message = responseController().messageFailUser
            else:
                _status = responseController().OK
                _message = responseController().messageOK
        except(Exception) as e:
            _status = responseController().interruption
            _message = responseController().messageInterruption + str(e)
            print('error: '+ str(e))
        return responseEntity(_status,_message,_userEntity).toJSON()
