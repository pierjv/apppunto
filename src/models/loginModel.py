from flask import Flask, jsonify, request
from src.cn.data_base_connection import Database
from src.models.dbModel import dbModel
from src.entities.userEntity import userEntity
from src.entities.userStoreEntity import userStoreEntity
from src.entities.loginEntity import loginEntity

class loginModel(dbModel):

    def __init__(self):
        dbModel.__init__(self)

    def login_user(self,loginEntity):
        _db = None
        _status = 1
        _userEntity = None
        try:
            _mail = loginEntity.mail
            _password = loginEntity.password
            _db = Database()
            _db.connect(self.host,self.port,self.user,self.password,self.database)
            print('Se conecto a la bd')
            _con_client = _db.get_client()

            _sql = """SELECT up.id,
                        up.mail ,
                        up.social_name ,
                        up.full_name ,
                        up.address ,
                        up.document_number ,
                        up.type_user ,
                        up.photo,
                        up.cellphone ,
                        up.about ,
                        s.full_name  AS service, 
                        s.url_image, 
                        ss.full_name AS sub_service, 
                        uss.enable
                    FROM   main.user_p up 
                        INNER JOIN main.user_service us 
                            ON up.id = us.id_user 
                        INNER JOIN main.service s 
                            ON us.id_service = s.id 
                        INNER JOIN main.user_sub_service uss 
                            ON up.id = uss.id_user 
                                AND uss.id_service = us.id_service 
                        LEFT JOIN main.sub_service ss 
                            ON uss.id_sub_service = ss.id
                    WHERE up.status = %s and up.mail = %s and up.password = %s;"""   

            _cur = _con_client.cursor()
            _cur.execute(_sql,(_status,_mail,_password,))
            _rows = _cur.fetchall()

            if len(_rows) >= 1:
                _userEntity= userEntity()
                _userEntity.id  = _rows[0][0]
                _userEntity.mail  = _rows[0][1] 
                _userEntity.social_name  = _rows[0][2]
                _userEntity.full_name  = _rows[0][3]
                _userEntity.address  = _rows[0][4]
                _userEntity.document_number  = _rows[0][5]
                _userEntity.type_user  = _rows[0][6]
                _userEntity.photo  = _rows[0][7]
                _userEntity.cellphone  = _rows[0][8]
                _userEntity.about  = _rows[0][9]

            _cur.close()
        except(Exception) as e:
            print('error: '+ str(e))
        finally:
            if _db is not None:
                _db.disconnect()
                print("Se cerro la conexion")
        return _userEntity