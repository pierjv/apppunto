from flask import Flask, jsonify, request
from src.cn.data_base_connection import Database
from src.models.dbModel import dbModel
from src.entities.userEntity import userEntity, typeDocumentEntity
from src.entities.userStoreEntity import userStoreEntity
from src.entities.loginEntity import loginEntity , loadEntity
from src.entities.customerEntity import customerEntity
from src.entities.serviceEntity import serviceEntity
from src.entities.subServiceEntity import subServiceEntity
import json


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
                        up.id_type_document ,
                        up.document_number ,
                        up.type_user ,
                        up.photo,
                        up.cellphone ,
                        up.about ,
                        s.full_name  AS service, 
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
                _userEntity.id_type_document  = _rows[0][4]
                _userEntity.document_number  = _rows[0][5]
                _userEntity.type_user  = _rows[0][6]
                _userEntity.cellphone  = _rows[0][7]
                _userEntity.about  = _rows[0][8]

            _cur.close()
        except(Exception) as e:
            print('error: '+ str(e))
        finally:
            if _db is not None:
                _db.disconnect()
                print("Se cerro la conexion")
        return _userEntity
    
    def login_customer(self,loginEntity):
        _db = None
        _status = 1
        _entity = None
        try:
            _mail = loginEntity.mail
            _password = loginEntity.password
            _db = Database()
            _db.connect(self.host,self.port,self.user,self.password,self.database)
            print('Se conecto a la bd')
            _con_client = _db.get_client()

            _sql = """SELECT id, 
                        mail, 
                        full_name, 
                        cellphone, 
                        photo
                    FROM   main.customer c 
                    WHERE  c.status = %s
                        AND c.mail = %s 
                        AND c."password" = %s; """   

            _cur = _con_client.cursor()
            _cur.execute(_sql,(_status,_mail,_password,))
            _rows = _cur.fetchall()

            if len(_rows) >= 1:
                _entity= customerEntity()
                _entity.id  = _rows[0][0]
                _entity.mail  = _rows[0][1] 
                _entity.full_name  = _rows[0][2]
                _entity.cellphone  = _rows[0][3]
                _entity.photo  = self.url_server + _rows[0][4]

            _cur.close()
        except(Exception) as e:
            print('error: '+ str(e))
        finally:
            if _db is not None:
                _db.disconnect()
                print("Se cerro la conexion")
        return _entity
    
    def get_load(self,id_customer):
        _db = None
        _status = 1
        _data_row = []
        _data_documents = []
        _data_users = []
        _id_customer = id_customer
        _loadEntity = None
        try:
            _loadEntity = loadEntity()
            _db = Database()
            _db.connect(self.host,self.port,self.user,self.password,self.database)
            print('Se conecto a la bd')
            _con_client = _db.get_client()
            _sql_services = """SELECT s.id, 
                        s.full_name, 
                        s.color,
                        encode(s.file_image , 'base64')  AS file_image, 
                        ss.id        AS id_sub_service, 
                        ss.full_name AS sub_service_name,
                        ss.in_filter
                    FROM   main.service s 
                        LEFT JOIN main.sub_service ss 
                                ON s.id = ss.id_service 
                    ORDER  BY 1;"""
                                        
            _cur = _con_client.cursor()
            _cur.execute(_sql_services)
            _rows = _cur.fetchall()
            _id_service_old = None
            for row in _rows:
                _serviceEntity = serviceEntity()
                _serviceEntity.id  = row[0]
                _serviceEntity.full_name  = row[1] 
                _serviceEntity.color  = row[2]
                _serviceEntity.file_image  = row[3].replace('\n','')
                _sub_service = row[4]
                _sub_services = []
                if _id_service_old  != _serviceEntity.id :
                    for se in _rows:
                        if row[0] == se[0] and _sub_service is not None:
                            _subServiceEntity = subServiceEntity()
                            _subServiceEntity.id = se[4]
                            _subServiceEntity.full_name = se[5]
                            _subServiceEntity.in_filter = se[6]
                            _sub_services.append(_subServiceEntity)

                    _serviceEntity.sub_services = _sub_services
                    _data_row.append(_serviceEntity)
                    _id_service_old = _serviceEntity.id 

            _loadEntity.services = _data_row

            _sql_services = """SELECT id, full_name FROM main.type_document WHERE status = 1;"""
            _cur.execute(_sql_services)
            _rows = _cur.fetchall()

            for row in _rows:
                _typeDocumentoEntity = typeDocumentEntity()
                _typeDocumentoEntity.id  = row[0]
                _typeDocumentoEntity.full_name  = row[1] 
                _data_documents.append(_typeDocumentoEntity)

            _loadEntity.type_documents = _data_documents

            if(_id_customer != 0):
                _sql_users = """SELECT a.id_user, 
                        b.avg_rate, 
                        up.mail, 
                        up.social_name, 
                        up.full_name, 
                        up.document_number, 
                        up.type_user, 
                        up.photo, 
                        up.cellphone, 
                        up.about,
                        up.id_type_document
                    FROM   (SELECT cr.id_customer, 
                                cr.id_user, 
                                Count(*) AS count_customer 
                            FROM   main.customer_rate cr 
                            WHERE  cr.id_customer = %s
                            GROUP  BY 1, 
                                    2) a 
                        INNER JOIN (SELECT cr.id_user, 
                                            Avg(rate) avg_rate, 
                                            Count(*)  count_rate 
                                    FROM   main.customer_rate cr 
                                    GROUP  BY 1) b 
                                ON a.id_user = b.id_user 
                        INNER JOIN main.user_p up 
                                ON up.id = a.id_user 
                    WHERE  up.status = %s"""
                                        
                _cur.execute(_sql_users,(_id_customer,_status,))
                _rows = _cur.fetchall()
                for row in _rows:
                    _serviceEntity = serviceEntity()
                    _userEntity = userEntity()
                    _userEntity.id =  row[0]
                    _userEntity.avg_rate  = str(row[1])
                    _userEntity.mail =  row[2]
                    _userEntity.social_name =  row[3]
                    _userEntity.full_name =  row[4]
                    _userEntity.document_number =  row[5]
                    _userEntity.type_user =  row[6]
                    _userEntity.photo =  row[7]
                    _userEntity.cellphone = row[8]
                    _userEntity.about =  row[9]
                    _userEntity.id_type_document = row[10]
                    _data_users.append(_userEntity)

            _loadEntity.preferred_users = _data_users
            _cur.close()
        except(Exception) as e:
            print('error: '+ str(e))
        finally:
            if _db is not None:
                _db.disconnect()
                print("Se cerro la conexion")
        return _loadEntity
    