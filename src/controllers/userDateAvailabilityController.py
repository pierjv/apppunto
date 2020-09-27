from src.models.userDateAvailabilityModel import userDateAvailabilityModel
from src.entities.responseEntity import responseEntity
from src.controllers.responseController import responseController
from src.entities.userDateAvailabilityEntity import userDateAvailabilityEntity, lstDateAvailabilityEntity

class userDateAvailabilityController(responseController):
    
    def get_user_date_availability_by_user(self,index):
        _message = None
        _status = None
        _data = None
        try:
            _model = userDateAvailabilityModel()
            _data = _model.get_user_date_availability_by_user(index)
            _status = self.OK
            _message = self.messageOK
        except(Exception) as e:
            _status = self.interruption
            _message = self.messageInterruption + str(e)
            print('error: '+ str(e))
        return responseEntity(_status,_message,_data).toJSON()
    
    def update_user_date_availability(self,request):
        _message = None
        _status = None
        _data = None
        _entity = None
        try:
            _model = userDateAvailabilityModel()
            _entity = lstDateAvailabilityEntity()
            _entity.requestToClass(request)
            _data = _model.update_user_date_availability(_entity)
            _status = self.OK
            _message = self.messageOK
        except(Exception) as e:
            _status = self.interruption
            _message = self.messageInterruption + str(e)
            print('error: '+ str(e))
        return responseEntity(_status,_message,_status).toJSON()