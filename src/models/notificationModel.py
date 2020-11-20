import requests
from src.cn.data_base_connection import Database
from src.models.dbModel import dbModel

class notificationModel(dbModel):

    def __init__(self):
        dbModel.__init__(self)
    
    def send_push_message(self, id_push_user,push_message):
        _response = None
        _value = None
        try:
            _post_data = {
                "to": id_push_user,
                "notification": {
                    "body": push_message,
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
            self.add_log(str(e),type(self).__name__)
        return _value

    def send_push_message_2(self, id_push_user):
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
            self.add_log(str(e),type(self).__name__)
        return _value
    
    def sen_sms_message(self,password,cellphone):
        try:
            params_data = {
                "action":"sendmessage",
                "username":self.text_user,
                "password":self.text_password,
                "recipient":cellphone,
                "messagedata":"Appunto: Hola tu clave es " + str(password) ,
                "longMessage":"false",
                "flash":"false",
                "premium":"false"   
            }
            r = requests.post(self.text_uri_get,params = params_data)
            print(r.text)
        except(Exception) as e:
            self.add_log(str(e),type(self).__name__)
    
    def send_sms_coupon(self,cellphone):
        try:
            params_data = {
                "action":"sendmessage",
                "username":self.text_user,
                "password":self.text_password,
                "recipient":cellphone,
                "messagedata":"Appunto: Tienes un nuevo cupon!" ,
                "longMessage":"false",
                "flash":"false",
                "premium":"false"   
            }
            r = requests.post(self.text_uri_get,params = params_data)
            print(r.text)
        except(Exception) as e:
            self.add_log(str(e),type(self).__name__)
    
    def send_sms_confirm_user(self,cellphone):
        try:
            params_data = {
                "action":"sendmessage",
                "username":self.text_user,
                "password":self.text_password,
                "recipient":cellphone,
                "messagedata":"Appunto: Tu Usuario ha sido validado, puedes ingresar al APP." ,
                "longMessage":"false",
                "flash":"false",
                "premium":"false"   
            }
            r = requests.post(self.text_uri_get,params = params_data)
            print(r.text)
        except(Exception) as e:
            self.add_log(str(e),type(self).__name__)


        

