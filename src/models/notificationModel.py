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
    
    def send_sms_refuse_user(self,cellphone):
        try:
            params_data = {
                "action":"sendmessage",
                "username":self.text_user,
                "password":self.text_password,
                "recipient":cellphone,
                "messagedata":"Appunto: Tu Usuario ha sido rechazado." ,
                "longMessage":"false",
                "flash":"false",
                "premium":"false"   
            }
            r = requests.post(self.text_uri_get,params = params_data)
            print(r.text)
        except(Exception) as e:
            self.add_log(str(e),type(self).__name__)

    def send_push_message_destination(self, ids_push,push_message):
        _response = None
        _value = None
        try:
            _post_data = {
                "to": ids_push,
                "notification": {
                    "body": push_message,
                    "title":"Appunto",
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

    def get_user_fire_base_token(self):
        _db = None
        _status = 1
        _data = []
        try:
            _db = Database()
            _db.connect(self.host,self.port,self.user,self.password,self.database)
            print('Se conecto a la bd')
            _con_client = _db.get_client()
            _sql = """SELECT up.id_fire_base_token
                        FROM main.user_p up 
                        WHERE up.id_fire_base_token IS NOT NULL
                        AND up.id_fire_base_token <> ''
                        AND up.status = %s; """
                                        
            _cur = _con_client.cursor()
            _cur.execute(_sql,(_status,))
            _rows = _cur.fetchall()

            for row in _rows:
                _data.append(row[0])

            _cur.close()
        except(Exception) as e:
            self.add_log(str(e),type(self).__name__)
        finally:
            if _db is not None:
                _db.disconnect()
                print("Se cerro la conexion")
        return _data

    def get_customer_fire_base_token(self):
        _db = None
        _status = 1
        _data = []
        try:
            _db = Database()
            _db.connect(self.host,self.port,self.user,self.password,self.database)
            print('Se conecto a la bd')
            _con_client = _db.get_client()
            _sql = """SELECT up.id_fire_base_token
                        FROM main.customer up 
                        WHERE up.id_fire_base_token IS NOT NULL
                        AND up.id_fire_base_token <> ''
                        AND up.status = %s; """
                                        
            _cur = _con_client.cursor()
            _cur.execute(_sql,(_status,))
            _rows = _cur.fetchall()

            for row in _rows:
                _data.append(row[0]) 

            _cur.close()
        except(Exception) as e:
            self.add_log(str(e),type(self).__name__)
        finally:
            if _db is not None:
                _db.disconnect()
                print("Se cerro la conexion")
        return _data
    



        

