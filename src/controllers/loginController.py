
from src.controllers.responseController import responseController
from src.models.loginModel import loginModel
from src.entities.loginEntity import loginEntity
from src.entities.responseEntity import responseEntity
from src.models.userModel import userModel
from src.entities.userEntity import userEntity
from src.models.serviceModel import serviceModel
from src.models.notificationModel import notificationModel
from src.models.customerModel  import customerModel
from src.entities.customerEntity import customerEntity

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
                _user_status = _userEntity.status
                if _user_status == self.status_user_to_be_confirmed:
                    _status = self.failUser
                    _message = self.messageUserToBeConfirmed
                    _userEntity = None
                
                if _user_status == self.status_user_refused:
                    _status = self.failUser
                    _message = self.messageUserToBeConfirmed
                    _userEntity = None

                if _user_status == self.status_user_confirmed:
                    _status = self.OK
                    _message = self.messageOK
                
        except(Exception) as e:
            _status = self.interruption
            _message = self.messageInterruption + str(e)
            print('error: '+ str(e))
        return responseEntity(_status,_message,_userEntity).toJSON()
    
    def recover_password_user(self,request):
        _message = None
        _status = self.interruption
        _entity = None
        _email = None
        try:
            _model = userModel()
            _entity  = userEntity()
            _entity.requestToEmail(request)
            _entity = _model.get_password_by_id(_entity.mail)
            if _entity is None :
                _status = self.failUser
                _message = self.userDontExist
            else:
                _modelLogin = notificationModel()
                _modelLogin.sen_sms_message(_entity.password,_entity.cellphone)
                _status = self.OK
                _message = self.smsSuccess + str(_entity.cellphone)

        except(Exception) as e:
            _status = self.interruption
            _message = self.messageInterruption + str(e)
            print('error: '+ str(e))
        return responseEntity(_status,_message,None).toJSON()

    def recover_password_customer(self,request):
        _message = None
        _status = self.interruption
        _entity = None
        _email = None
        try:
            _model = customerModel()
            _entity  = customerEntity()
            _entity.requestToEmail(request)
            _entity = _model.get_password_by_id(_entity.mail)
            if _entity is None :
                _status = self.failUser
                _message = self.userDontExist
            else:
                _modelLogin = notificationModel()
                _modelLogin.sen_sms_message(_entity.password,_entity.cellphone)
                _status = self.OK
                _message = self.smsSuccess + str(_entity.cellphone)

        except(Exception) as e:
            _status = self.interruption
            _message = self.messageInterruption + str(e)
            print('error: '+ str(e))
        return responseEntity(_status,_message,None).toJSON()

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
    
    def get_load(self,index):
        _message = None
        _status = None
        _data= None
        try:
            _model = loginModel()
            _id_customer = index
            _data = _model.get_load(_id_customer)
            _status = self.OK
            _message = self.messageOK
        except(Exception) as e:
            _status = self.interruption
            _message = self.messageInterruption + str(e)
            print('error: '+ str(e))
        return responseEntity(_status,_message,_data).toJSON()
    
    def login_user_web(self,full_name,password):
        _entity = None
        try:
            _model = loginModel()
            _entity = _model.login_user_web(full_name,password)
        except(Exception) as e:
            print('error: '+ str(e))
        return _entity
    
    def change_password_user_web(self,full_name,password):
        _full_name = None
        try:
            _model = loginModel()
            _full_name = _model.change_password_user_web(full_name,password)
        except(Exception) as e:
            print('error: '+ str(e))
        return _full_name