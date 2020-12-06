from src.models.userModel import userModel
from src.entities.userEntity import userEntity,lstuserServiceAddEntity, lstUserSubServiceAddEntity, userBankEntity,userSubServiceFilterEntity
from src.entities.responseEntity import responseEntity
from src.controllers.responseController import responseController
from src.models.notificationModel import notificationModel

class userController(responseController):

    def get_users(self):
        _message = None
        _status = self.interruption
        _data= None
        try:
            _userModel = userModel()
            _data = _userModel.get_users()
            _status = self.OK
            _message = self.messageOK
        except(Exception) as e:
            _status = self.interruption
            _message = self.messageInterruption + str(e)
            print('error: '+ str(e))
        return responseEntity(_status,_message,_data).toJSON()
    
    def get_users_by_type(self,index):
        _message = None
        _status = self.interruption
        _data= None
        _type_user = None
        try:
            _userModel = userModel()

            if index == self.idTypeUserMarca:
                _type_user = self.typeUserMarca
            if index == self.idTypeUserFreelancer:
                _type_user = self.typeUserFreelancer
                
            _data = _userModel.get_users_by_type(_type_user)
            _status = self.OK
            _message = self.messageOK
        except(Exception) as e:
            _status = self.interruption
            _message = self.messageInterruption + str(e)
            print('error: '+ str(e))
        return responseEntity(_status,_message,_data).toJSON()
    
    def get_users_by_type_sub_services(self,request):
        _message = None
        _status = self.interruption
        _data= None
        _type_user = None
        try:
            _userModel = userModel()
            _entity = userSubServiceFilterEntity()
            _entity.requestToClass(request)                
            _data = _userModel.get_users_by_type_sub_services(_entity)
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
                _entity = _model.add_user(_entity,self.status_user_to_be_confirmed)
                _status = self.status_user_to_be_confirmed_admin
                _message = self.messageUserToBeConfirmedAdmin
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
    
    def update_user(self,request):
        _message = ''
        _status = self.interruption
        _userEntity= None
        try:
            _userEntity = userEntity()
            _userModel = userModel()
            _userEntity.requestUpdateToClass(request)
            _id = _userModel.update_user(_userEntity)
            _status = self.OK
            _message = self.messageOK
        except(Exception) as e:
            _status = self.interruption
            _message = self.messageInterruption +str(e)
            print('error: '+ str(e))
        return responseEntity(_status,_message,_id).toJSON()

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

    def get_user_by_sub_services(self,request):
        _message = None
        _status = self.interruption
        _data = None
        try:
            _model = userModel() 
            _entity = userEntity()
            _sub_service = _entity.requestSubServiceToString(request)
            print(_sub_service)
            _data = _model.get_user_by_sub_services(_sub_service)
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
    
    def get_user_detail(self,index,id_customer):
        _message = None
        _status = None
        _data= None
        try:
            _model = userModel()
            _data = _model.get_user_detail(index,id_customer)
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

    def update_user_service(self,request):
        _message = ''
        _status = self.interruption
        _entity= None
        _data = []
        try:
            _entity = lstuserServiceAddEntity()
            _userModel = userModel()
            _entity.requestToClass(request)
            _data = _userModel.update_user_service(_entity.user_services)
            _status = self.OK
            _message = self.messageOK
        except(Exception) as e:
            _status = self.interruption
            _message = self.messageInterruption +str(e)
            print('error: '+ str(e))
        return responseEntity(_status,_message,_data).toJSON()

    
    def get_dashboard_mobile(self,index):
        _message = None
        _status = self.interruption
        _data = None
        try:
            _model = userModel()
            _data = _model.get_dashboard_mobile(index)
            _status = self.OK
            _message = self.messageOK
        except(Exception) as e:
            _status = self.interruption
            _message = self.messageInterruption +str(e)
            print('error: '+ str(e))
        return responseEntity(_status,_message,_data).toJSON()

    def update_user_sub_service(self,request):
        _message = ''
        _status = self.interruption
        _entity= None
        _data = []
        try:
            _entity = lstUserSubServiceAddEntity()
            _userModel = userModel()
            _entity.requestToClass(request)
            _data = _userModel.update_user_sub_service(_entity.user_sub_services)
            _status = self.OK
            _message = self.messageOK
        except(Exception) as e:
            _status = self.interruption
            _message = self.messageInterruption +str(e)
            print('error: '+ str(e))
        return responseEntity(_status,_message,_data).toJSON()
    
    def get_user_bank_account_by_id_user(self,index):
        _message = None
        _status = self.interruption
        _data= None
        try:
            _model = userModel()
            _data = _model.get_user_bank_account_by_id_user(index)
            _status = self.OK
            _message = self.messageOK
        except(Exception) as e:
            _status = self.interruption
            _message = self.messageInterruption + str(e)
            print('error: '+ str(e))
        return responseEntity(_status,_message,_data).toJSON()
    
    def add_user_bank_account(self,request):
        _message = None
        _status = self.interruption
        _data= None
        try:
            _entity = userBankEntity()
            _entity.requestToClass(request)
            _model = userModel()
            _data = _model.add_user_bank_account(_entity)
            _status = self.OK
            _message = self.messageOK
        except(Exception) as e:
            _status = self.interruption
            _message = self.messageInterruption + str(e)
            print('error: '+ str(e))
        return responseEntity(_status,_message,_data).toJSON()

    def update_user_bank_account(self,request):
        print(1)
        _message = None
        _status = self.interruption
        _data= None
        try:
            _entity = userBankEntity()
            _entity.requestUpdateToClass(request)
            _model = userModel()
            _data = _model.update_user_bank_account(_entity)
            print(_data)
            _status = self.OK
            _message = self.messageOK
        except(Exception) as e:
            _status = self.interruption
            _message = self.messageInterruption + str(e)
            print('error: '+ str(e))
        return responseEntity(_status,_message,_data).toJSON()
    
    def delete_user_bank_account(self,index):
        _message = None
        _status = self.interruption
        id_customer_address= None
        try:
            _model = userModel()
            id_customer_address = _model.delete_user_bank_account(index)
            _status = self.OK
            _message = self.messageOK
        except(Exception) as e:
            _status = self.interruption
            _message = self.messageInterruption + str(e)
            print('error: '+ str(e))
        return responseEntity(_status,_message,id_customer_address).toJSON()

    def get_users_wa(self):
        _data= None
        try:
            _userModel = userModel()
            _data = _userModel.get_users_wa()
        except(Exception) as e:
            print('error: '+ str(e))
        return _data

    def confirm_user_status(self,index):
        _data= None
        try:
            _userModel = userModel()
            _notificationModel = notificationModel()
            _entity = _userModel.get_user_by_id(index)
            _data = _userModel.update_user_status(index,self.status_user_confirmed)
            _notificationModel.send_sms_confirm_user(_entity.cellphone)
             
        except(Exception) as e:
            print('error: '+ str(e))
        return _data
    
    def refuse_user_status(self,index):
        _data= None
        try:
            _userModel = userModel()
            _notificationModel = notificationModel()
            _entity = _userModel.get_user_by_id(index)
            _data = _userModel.update_user_status(index,self.status_user_refused)
            _notificationModel.send_sms_refuse_user(_entity.cellphone)
             
        except(Exception) as e:
            print('error: '+ str(e))
        return _data
    
    def update_coupon_status_wa(self,status):
        _data= None
        try:
            _model = userModel()
            _data = _model.update_coupon_status_wa(status)
        except(Exception) as e:
            print('error: '+ str(e))
        return _data

    def get_coupon_status_wa(self):
        _data= None
        try:
            _model = userModel()
            _data = _model.get_coupon_status_wa()
        except(Exception) as e:
            print('error: '+ str(e))
        return _data
