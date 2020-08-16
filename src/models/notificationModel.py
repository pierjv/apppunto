import requests
from src.cn.data_base_connection import Database
from src.models.dbModel import dbModel

class notificationModel(dbModel):

    def __init__(self):
        dbModel.__init__(self)
    
    def send_push_message(self, id_push_user):
        _response = None
        _value = None
        try:
            _post_data = {
                "to": id_push_user,
                "notification": {
                    "body":"Tienes una nueva solicitud con cuerpo",
                    "title":"Solicitud",
                    "content_available" : True,
                    "priority" : "high"
                },
                "data" : {
                    "contents" :  {"type":1,"body":"cuerpo json"}
                }
            }
            _headers = {"Authorization": self.push_firebase_key}
            _response = requests.post(url=self.push_uri_post, json=_post_data,headers=_headers)
            _value = _response.text
        except(Exception) as e:
             print('error: '+ str(e))
        return _value
