from flask import Flask, jsonify, request
from src.cn.data_base_connection import Database
from src.models.dbModel import dbModel
from src.entities.userEntity import userEntity, typeDocumentEntity, bankEntity
from src.entities.userStoreEntity import userStoreEntity
from src.entities.loginEntity import loginEntity , loadEntity
from src.entities.customerEntity import customerEntity 
from src.entities.serviceEntity import serviceEntity
from src.entities.subServiceEntity import subServiceEntity
from src.entities.saleEntity import deliveryCost
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

            _sql = """ SELECT up.id,
                        up.mail ,
                        up.social_name ,
                        up.full_name ,
                        up.id_type_document ,
                        up.document_number ,
                        up.type_user ,
                        up.photo,
                        up.cellphone ,
                        up.about,
                        a.avg_rate,
                        up.status
                    FROM   main.user_p up
                        LEFT JOIN (SELECT id_user, 
                                        Avg(rate) :: float4 AS avg_rate 
                                FROM   main.customer_rate 
                                GROUP  BY 1) a 
                            ON a.id_user = up.id  
                    WHERE up.mail = %s and up.password = %s;"""   

            _cur = _con_client.cursor()
            _cur.execute(_sql,(_mail,_password,))
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
                _userEntity.photo = _rows[0][7]
                _userEntity.cellphone  = _rows[0][8]
                _userEntity.about  = _rows[0][9]
                _avg_rate =  _rows[0][10]
                if _avg_rate is None:
                    _avg_rate = 0
                _userEntity.avg_rate = _avg_rate
                _userEntity.status = _rows[0][11]

                _sql_fire_base = """UPDATE main.user_p SET id_fire_base_token = %s WHERE id = %s;"""
                _cur.execute(_sql_fire_base, (loginEntity.id_fire_base_token,_userEntity.id,))
                _con_client.commit()

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

            _sql = """SELECT c.id, 
                        mail, 
                        full_name, 
                        cellphone, 
                        photo,
                        id_code,
                        referred_code,
                        ca.id as id_customer_address
                    FROM   main.customer c 
                    INNER JOIN main.customer_address ca 
                    	on c.id  = ca.id_customer 
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
                _entity.photo  =  _rows[0][4]
                _entity.id_code  =  _rows[0][5]
                _entity.referred_code  =  _rows[0][6]
                _entity.id_customer_address = _rows[0][7]

                _sql_fire_base = """UPDATE main.customer SET id_fire_base_token = %s WHERE id = %s;"""
                _cur.execute(_sql_fire_base, (loginEntity.id_fire_base_token,_entity.id,))
                _con_client.commit()

            _cur.close()
        except(Exception) as e:
            self.add_log(str(e),type(self).__name__)
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
        _data_delivery_costs = []
        _data_banks= []
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
                    WHERE s.status = 1
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
                            _subServiceEntity.id_service = se[0]
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

            _sql_delivery = """SELECT from_km, to_km, fixed_cost, delivery FROM main.delivery_cost;"""
            _cur.execute(_sql_delivery)
            _rows = _cur.fetchall()

            for row in _rows:
                _delivery_cost = deliveryCost()
                _delivery_cost.from_km  = row[0]
                _delivery_cost.to_km  = row[1] 
                _delivery_cost.fixed_cost  = row[2]
                _delivery_cost.delivery  = row[3]
                _data_delivery_costs.append(_delivery_cost)

            _loadEntity.delivery_costs = _data_delivery_costs

            _sql_banks = """SELECT id, full_name FROM main.bank WHERE status = 1;"""
            _cur.execute(_sql_banks)
            _rows = _cur.fetchall()

            for row in _rows:
                _bankEntity = bankEntity()
                _bankEntity.id  = row[0]
                _bankEntity.full_name  = row[1] 
                _data_banks.append(_bankEntity)

            _loadEntity.banks = _data_banks

            if(_id_customer != 0):
                _sql_users = """SELECT u.id, 
                                u.mail, 
                                u.social_name, 
                                u.full_name, 
                                u.id_type_document, 
                                u.document_number, 
                                u.type_user, 
                                u.photo, 
                                u.cellphone, 
                                u.about, 
                                us.id        AS id_user_store, 
                                us.full_name AS name_user_store, 
                                us.address, 
                                us.longitude, 
                                us.latitude, 
                                us.main, 
                                b.avg_rate::float4
                            FROM   main.user_p u 
                            INNER JOIN main.user_store us 
                                        ON u.id = us.id_user
                            INNER JOIN main.customer_user_favorite  cf
                                    ON u.id = cf.id_user 
                            LEFT JOIN (SELECT cr.id_user, 
                                                Avg(rate) avg_rate, 
                                                Count(*)  count_rate 
                                        FROM   main.customer_rate cr 
                                        GROUP  BY 1) b 
                                    ON u.id = b.id_user  
                        WHERE  cf.id_customer = %s and u.status = %s and cf."enable" = 1 AND us.status = 1 
                        ORDER BY 1;"""
                                        
                _cur.execute(_sql_users,(_id_customer,_status,))
                _rows = _cur.fetchall()
                _id_user_old = None
                for row in _rows:
                    _userEntity= userEntity()
                    _userEntity.id  = row[0]
                    _userEntity.mail  = row[1] 
                    _userEntity.social_name  = row[2]
                    _userEntity.full_name  = row[3]
                    _userEntity.id_type_document  = row[4]
                    _userEntity.document_number  = row[5]
                    _userEntity.type_user  = row[6]
                    _userEntity.photo  = row[7]
                    _userEntity.cellphone  = row[8]
                    _userEntity.about  = row[9]
                    _avg_rate =  row[16]
                    if _avg_rate is None:
                        _avg_rate = 0
                    _userEntity.avg_rate = _avg_rate
                    _user_stores = []
                    if _id_user_old  != _userEntity.id :
                        for se in _rows:
                            if row[0] == se[0] and _userEntity is not None:
                                _userStoreEntity = userStoreEntity()
                                _userStoreEntity.id = se[10]
                                _userStoreEntity.full_name = se[11]
                                _userStoreEntity.address = se[12]
                                _userStoreEntity.longitude = se[13]
                                _userStoreEntity.latitude = se[14]
                                _userStoreEntity.main = se[15]
                                _userStoreEntity.id_user = _userEntity.id 
                                _user_stores.append(_userStoreEntity)

                        _userEntity.user_store = _user_stores
                        _data_users.append(_userEntity)
                        _id_user_old = _userEntity.id 

            _loadEntity.preferred_users = _data_users
            _cur.close()
        except(Exception) as e:
            self.add_log(str(e),type(self).__name__)
        finally:
            if _db is not None:
                _db.disconnect()
                print("Se cerro la conexion")
        return _loadEntity
    
    def login_user_web(self,full_name,password):
        _db = None
        _status = 1
        _entity = None
        try:
            _full_name = full_name
            _password = password
            _db = Database()
            _db.connect(self.host,self.port,self.user,self.password,self.database)
            print('Se conecto a la bd')
            _con_client = _db.get_client()

            _sql = """SELECT u.id, 
                        u.full_name
                    FROM   main.user_web u 
                    WHERE  u.status = %s
                        AND u.full_name = %s 
                        AND u."password" = %s; """   

            _cur = _con_client.cursor()
            _cur.execute(_sql,(_status,_full_name,_password,))
            _rows = _cur.fetchall()

            if len(_rows) >= 1:
                _entity = userEntity()
                _entity.id  = _rows[0][0]
                _entity.full_name  = _rows[0][1] 

            _cur.close()
        except(Exception) as e:
            self.add_log(str(e),type(self).__name__)
        finally:
            if _db is not None:
                _db.disconnect()
                print("Se cerro la conexion")
        return _entity
    
    def change_password_user_web(self,full_name,password):
        _db = None
        _status = 1
        try:
            _db = Database()
            _db.connect(self.host,self.port,self.user,self.password,self.database)
            print('Se conecto a la bd')
            _con_client = _db.get_client()
            _sql = """UPDATE main.user_web SET "password" = %s WHERE full_name = %s AND status = %s;"""
            _cur = _con_client.cursor()
            _cur.execute(_sql, (password,full_name,_status,))
            _con_client.commit()
            _cur.close()
        except(Exception) as e:
            self.add_log(str(e),type(self).__name__)
        finally:
            if _db is not None:
                _db.disconnect()
                print("Se cerro la conexion")
        return full_name