from src.models.saleModel import saleModel
from src.entities.saleEntity import saleEntity , saleConfirmEntity
from src.entities.responseEntity import responseEntity
from src.controllers.responseController import responseController
from src.models.chargeModel import chargeModel
from src.models.notificationModel import notificationModel

class saleController(responseController):

    def add_sale_reserve(self,request):
        _message = None
        _status = self.interruption
        _entity= None
        _response = None
        _id_push_user = "fN0WAicAdUH5qjVMgD3Api:APA91bEBaRiXlVw0Rh3PhclAQmU0LHfc3zJxPQLIx2mjbtFoQFWqApfpHm6w4x-9_qBehL1jpgVds9a0cm-u6jtDZD4V784F1152yAqrdP_fNr8uMo7POQBRQmM2b-4TLuc287J79WQu"
        try:
            _entity = saleEntity()
            _model = saleModel()
            _notificationModel = notificationModel()
            _chargeModel = chargeModel()
            _entity.requestToClass(request)
            _entity = _model.add_sale_reserve(_entity)
            _response = _notificationModel.send_push_message(_id_push_user)
            print(_response)
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


