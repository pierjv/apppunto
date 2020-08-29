from src.models.saleModel import saleModel
from src.entities.saleEntity import saleEntity
from src.entities.responseEntity import responseEntity
from src.controllers.responseController import responseController
from src.models.chargeModel import chargeModel

class saleController(responseController):

    def add_sale(self,request):
        _message = None
        _status = self.interruption
        _entity= None
        try:
            _entity = saleEntity()
            _model = saleModel()
            _chargeModel = chargeModel()
            _entity.requestToClass(request)
            _data = _chargeModel.charge_culqi(_entity.cvv,_entity.document_number,_entity.expiration_year,_entity.expiration_month,
                    _entity.mail,_entity.total_amount, "Venta Appunto")
            if _data["object"] == "error":
                _status = self.interruption
                _message = _data["user_message"]
            else:
                _entity = _model.add_sale(_entity)
                _status = self.OK
                _message = self.saleSuccess
                
        except(Exception) as e:
            _status = self.interruption
            _message = self.messageInterruption +str(e)
            print('error: '+ str(e))
        return responseEntity(_status,_message,_entity).toJSON()

