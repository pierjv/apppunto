from src.models.saleModel import saleModel
from src.entities.saleEntity import saleEntity
from src.entities.responseEntity import responseEntity
from src.controllers.responseController import responseController

class saleController(responseController):

    def add_sale(self,request):
        _message = None
        _status = responseController().interruption
        _entity= None
        try:
            _entity = saleEntity()
            _model = saleModel()
            _entity.requestToClass(request)
            _entity = _model.add_sale(_entity)
            _status = responseController().OK
            _message = responseController().messageOK
                
        except(Exception) as e:
            _status = responseController().interruption
            _message = responseController().messageInterruption +str(e)
            print('error: '+ str(e))
        return responseEntity(_status,_message,_entity).toJSON()

