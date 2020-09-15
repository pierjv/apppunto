from src.models.saleModel import saleModel
from src.entities.saleEntity import saleEntity , saleConfirmEntity
from src.entities.responseEntity import responseEntity
from src.controllers.responseController import responseController
from src.models.chargeModel import chargeModel
from src.models.notificationModel import notificationModel
from src.models.userModel import userModel
from src.models.customerModel import customerModel

class saleController(responseController):

    def add_sale_reserve(self,request):
        _message = None
        _status = self.interruption
        _entity= None
        _response = None
        _id_fire_base_token = None
        try:
            _entity = saleEntity()
            _model = saleModel()
            _userModel =userModel()
            _notificationModel = notificationModel()
            _chargeModel = chargeModel()
            _entity.requestToClass(request)
            _entity = _model.add_sale_reserve(_entity)
            _id_fire_base_token = _userModel.get_id_fire_base_token_by_id_user(_entity.id_user)
            if _id_fire_base_token is not None:
                _response = _notificationModel.send_push_message(_id_fire_base_token,self.push_message_user)
            if _response is None :
                _status = self.OK
                _message = self.saleSuccess
            else:
                _status = self.OK
                _message = self.saleSuccessNotPush
                
        except(Exception) as e:
            _status = self.interruption
            _message = self.messageInterruption +str(e)
            print('error: '+ str(e))
        return responseEntity(_status,_message,_entity).toJSON()

    def add_sale_confirm(self,request):
        _message = None
        _status = self.interruption
        _entity= None
        _response = None
        try:

            _entity = saleConfirmEntity()
            _model = saleModel()
            _chargeModel = chargeModel()
            _entity.requestToClass(request)
            
            _data = _chargeModel.charge_culqi(_entity.cvv,_entity.document_number,_entity.expiration_year,_entity.expiration_month,
            _entity.mail,_entity.total_amount, "Venta Appunto")
            if _data["object"] == "error":
                _status = self.interruption
                _message = _data["user_message"]
            else:
                print(_entity.id_sale)
                _entity = _model.add_sale_confirm(_entity.id_sale)
                _status = self.OK
                _message = self.saleSuccessConfirm

        except(Exception) as e:
            _status = self.interruption
            _message = self.messageInterruption +str(e)
            print('error: '+ str(e))
        return responseEntity(_status,_message,_entity).toJSON()

    def add_sale_2(self,request):
        _message = None
        _status = self.interruption
        _entity= None
        try:
            _entity = saleEntity()
            _model = saleModel()
            _chargeModel = chargeModel()
            _entity.requestToClass(request)
            _data = _chargeModel.charge_culqi("cvv",_entity.document_number,_entity.expiration_year,_entity.expiration_month,
                    _entity.mail,_entity.total_amount, "Venta Appunto")
            if _data["object"] == "error":
                _status = self.interruption
                _message = _data["user_message"]
            else:
                _entity = _model.add_sale_reserve(_entity)
                _status = self.OK
                _message = self.saleSuccess
                
        except(Exception) as e:
            _status = self.interruption
            _message = self.messageInterruption +str(e)
            print('error: '+ str(e))
        return responseEntity(_status,_message,_entity).toJSON()

    def get_sale_by_id_sale(self,index):
        _message = None
        _status = self.interruption
        _entity= None
        try:
            _model = saleModel()
            _entity = _model.get_sale_by_id_sale(index)
            _status = self.OK
            _message = self.messageOK
        except(Exception) as e:
            _status = self.interruption
            _message = self.messageInterruption + str(e)
            print('error: '+ str(e))
        return responseEntity(_status,_message,_entity).toJSON()

    def get_sale_by_id_customer(self,index):
        _message = None
        _status = self.interruption
        _entity= None
        try:
            _model = saleModel()
            _entity = _model.get_sale_by_id_customer(index)
            _status = self.OK
            _message = self.messageOK
        except(Exception) as e:
            _status = self.interruption
            _message = self.messageInterruption + str(e)
            print('error: '+ str(e))
        return responseEntity(_status,_message,_entity).toJSON()

    def get_sale_by_id_user(self,index):
        _message = None
        _status = self.interruption
        _entity= None
        try:
            _model = saleModel()
            _entity = _model.get_sale_by_id_user(index)
            _status = self.OK
            _message = self.messageOK
        except(Exception) as e:
            _status = self.interruption
            _message = self.messageInterruption + str(e)
            print('error: '+ str(e))
        return responseEntity(_status,_message,_entity).toJSON()

    def accept_sale(self,index):
        _message = None
        _status = self.interruption
        _id_sale= None
        _id_fire_base_token = None
        try:
            _model = saleModel()
            _customerModel = customerModel()
            _notificationModel = notificationModel()
            _id_sale = _model.update_status_sale(index,self.status_sale_accept)
            _id_customer = _model.get_id_customer_by_id_sale(index)
            _id_fire_base_token = _customerModel.get_id_fire_base_token_by_id_customer(_id_customer)

            if _id_fire_base_token is not None:
                _response = _notificationModel.send_push_message(_id_fire_base_token,self.push_message_accept_sale)

            if _response is None :
                _status = self.OK
                _message = self.pushSuccess
            else:
                _status = self.OK
                _message = self.pushNotSuccess
        except(Exception) as e:
            _status = self.interruption
            _message = self.messageInterruption + str(e)
            print('error: '+ str(e))
        return responseEntity(_status,_message,_id_sale).toJSON()

    
    def refuse_sale(self,index):
        _message = None
        _status = self.interruption
        _id_sale= None
        _id_fire_base_token = None
        try:
            _model = saleModel()
            _customerModel = customerModel()
            _notificationModel = notificationModel()
            _id_sale = _model.update_status_sale(index,self.status_sale_refuse)
            _id_customer = _model.get_id_customer_by_id_sale(index)
            _id_fire_base_token = _customerModel.get_id_fire_base_token_by_id_customer(_id_customer)

            if _id_fire_base_token is not None:
                _response = _notificationModel.send_push_message(_id_fire_base_token,self.push_message_refuse_sale)
            print(_response)
            if _response is None :
                _status = self.OK
                _message = self.pushSuccess
            else:
                _status = self.OK
                _message = self.pushNotSuccess
        except(Exception) as e:
            _status = self.interruption
            _message = self.messageInterruption + str(e)
            print('error: '+ str(e))
        return responseEntity(_status,_message,_id_sale).toJSON()


