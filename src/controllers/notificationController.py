import requests
import json 
from src.controllers.responseController import responseController
from src.models.notificationModel import notificationModel
from src.entities.responseEntity import responseEntity

class notificationController(responseController):

    def send_push_message(self):
        _message = None
        _status = self.interruption
        _response = None
        _id_push_user = "fN0WAicAdUH5qjVMgD3Api:APA91bEBaRiXlVw0Rh3PhclAQmU0LHfc3zJxPQLIx2mjbtFoQFWqApfpHm6w4x-9_qBehL1jpgVds9a0cm-u6jtDZD4V784F1152yAqrdP_fNr8uMo7POQBRQmM2b-4TLuc287J79WQu"
        try:
            _model = notificationModel()
            _response = _model.send_push_message(_id_push_user)
            if _response is None :
                _status = self.interruption
                _message = self.messageInterruption
            else:
                _status = self.OK
                _message = self.messageOK
                _response = json.loads(_response)
        except(Exception) as e:
            _status = self.interruption
            _message = self.messageInterruption + str(e)
            print('error: '+ str(e))
        return responseEntity(_status,_message,_response).toJSON()
