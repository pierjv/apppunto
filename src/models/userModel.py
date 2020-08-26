from flask import Flask, jsonify, request
from src.cn.data_base_connection import Database
from src.models.dbModel import dbModel
from src.entities.userEntity import userEntity,userDetailEntity,rateEntity,commentEntity
from src.entities.serviceEntity import serviceEntity
from src.entities.subServiceEntity import subServiceEntity


class userModel(dbModel):

    def __init__(self):
        dbModel.__init__(self)

    def add_user(self,userEntity):
        _db = None
        _id_user = 0
        _status = 1
        _i = 0
        try:
            _db = Database()
            _db.connect(self.host,self.port,self.user,self.password,self.database)
            print('Se conecto a la bd')
            _con_client = _db.get_client()
            _sql = """INSERT INTO main.user_p (mail,social_name,full_name,document_number,type_user,photo,
                      cellphone,about,password,id_type_document,status) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id;"""
            _cur = _con_client.cursor()
            _cur.execute(_sql, (userEntity.mail,userEntity.social_name,userEntity.full_name,
                                userEntity.document_number,userEntity.type_user,
                                userEntity.photo,userEntity.cellphone,userEntity.about,userEntity.password,
                                userEntity.id_type_document,_status))
            _id_user = _cur.fetchone()[0]
            userEntity.id = _id_user
            
            _sql_store = """INSERT INTO main.user_store (id_user, full_name, address, longitude, latitude, main, status) 
                            VALUES(%s,%s,%s,%s,%s,%s,%s) RETURNING id;"""
            for us in userEntity.user_store:
                _cur.execute(_sql_store, (_id_user,us.full_name,us.address,us.longitude,us.latitude,us.main,_status))
                _id_user_store = _cur.fetchone()[0]
                userEntity.user_store[_i].id = _id_user_store
                userEntity.user_store[_i].id_user = _id_user
                _i += 1

            _con_client.commit()
            _cur.close()
        except(Exception) as e:
            self.add_log(str(e),type(self).__name__)
        finally:
            if _db is not None:
                _db.disconnect()
                print("Se cerro la conexion")
        return userEntity

    def delete_user(self,id):
        _db = None
        _status = 0
        _id = id
        try:
            _db = Database()
            _db.connect(self.host,self.port,self.user,self.password,self.database)
            print('Se conecto a la bd')
            _con_client = _db.get_client()
            _sql = """UPDATE main.user_p SET status = %s WHERE id = %s;"""
            _cur = _con_client.cursor()
            _cur.execute(_sql, (_status,_id))
            _con_client.commit()
            _cur.close()
        except(Exception) as e:
            self.add_log(str(e),type(self).__name__)
        finally:
            if _db is not None:
                _db.disconnect()
                print("Se cerro la conexion")
        return _id
    
    def get_users(self):
        _db = None
        _status = 0
        _id = id
        _data_row = []
        try:
            _db = Database()
            _db.connect(self.host,self.port,self.user,self.password,self.database)
            print('Se conecto a la bd')
            _con_client = _db.get_client()
            _sql = """SELECT id, mail, social_name, full_name, id_type_document, document_number, type_user, photo, 
                      cellphone, about FROM main.user_p WHERE status = 1;"""
            _cur = _con_client.cursor()
            _cur.execute(_sql)
            _rows = _cur.fetchall()

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
                _data_row.append(_userEntity)

            _cur.close()
        except(Exception) as e:
            self.add_log(str(e),type(self).__name__)
        finally:
            if _db is not None:
                _db.disconnect()
                print("Se cerro la conexion")
        return _data_row

    def get_user_by_id(self,id):
        _db = None
        _status = 1
        _entity = None
        _id_user = id
        try:
            _db = Database()
            _db.connect(self.host,self.port,self.user,self.password,self.database)
            print('Se conecto a la bd')
            _con_client = _db.get_client()

            _sql = """SELECT up.id, 
                        up.mail, 
                        up.social_name, 
                        up.full_name, 
                        up.id_type_document, 
                        up.document_number, 
                        up.type_user, 
                        up.photo, 
                        up.cellphone,
                        up.about
                    FROM   main.user_p up 
                    WHERE  up.status = %s
                        AND id = %s; """   

            _cur = _con_client.cursor()
            _cur.execute(_sql,(_status,_id_user,))
            _rows = _cur.fetchall()
        
            if len(_rows) >= 1:
                _entity= userEntity()
                _entity.id  = _rows[0][0]
                _entity.mail  = _rows[0][1] 
                _entity.social_name  = _rows[0][2]
                _entity.full_name  = _rows[0][3]
                _entity.id_type_document  = _rows[0][4]
                _entity.document_number  = _rows[0][5]
                _entity.type_user  = _rows[0][6]
                _entity.photo  = _rows[0][7]
                _entity.cellphone  = _rows[0][8]
                _entity.about  = _rows[0][9]

            _cur.close()
        except(Exception) as e:
            self.add_log(str(e),type(self).__name__)
        finally:
            if _db is not None:
                _db.disconnect()
                print("Se cerro la conexion")
        return _entity

    def get_password_by_id(self,email):
        _db = None
        _status = 1
        _entity = None
        _mail = email
        try:
            _db = Database()
            _db.connect(self.host,self.port,self.user,self.password,self.database)
            print('Se conecto a la bd')
            _con_client = _db.get_client()

            _sql = """SELECT up."password", up.cellphone
                    FROM   main.user_p up 
                    WHERE  up.status = %s
                        AND mail = %s; """   

            _cur = _con_client.cursor()
            _cur.execute(_sql,(_status,_mail,))
            _rows = _cur.fetchall()
        
            if len(_rows) >= 1:
                _entity  = userEntity()
                _entity.password = _rows[0][0]
                _entity.cellphone = _rows[0][1]

            _cur.close()
        except(Exception) as e:
            self.add_log(str(e),type(self).__name__)
        finally:
            if _db is not None:
                _db.disconnect()
                print("Se cerro la conexion")
        return _entity

    def get_user_by_id_service(self,idService):
        _db = None
        _status = 1
        _id_service = idService
        _data_row =[]
        try:
            _db = Database()
            _db.connect(self.host,self.port,self.user,self.password,self.database)
            print('Se conecto a la bd')
            _con_client = _db.get_client()

            _sql = """SELECT up.id, 
                        up.mail, 
                        up.social_name, 
                        up.full_name, 
                        up.id_type_document, 
                        up.document_number, 
                        up.type_user, 
                        up.photo, 
                        up.status, 
                        up.cellphone, 
                        up.about
                    FROM   main.user_p up 
                        INNER JOIN main.user_service us 
                                ON up.id = us.id_user 
                    WHERE  up.status = %s 
                        AND us.id_service = %s;"""   

            _cur = _con_client.cursor()
            _cur.execute(_sql,(_status,_id_service,))
            _rows = _cur.fetchall()

            for row in _rows:
                _entity= userEntity()
                _entity.id  = row[0]
                _entity.mail  = row[1] 
                _entity.social_name  = row[2]
                _entity.full_name  = row[3]
                _entity.id_type_document  = row[4]
                _entity.document_number  = row[5]
                _entity.type_user  = row[6]
                _entity.photo  = row[7]
                _entity.cellphone  = row[8]
                _entity.about  = row[9]
                _data_row.append(_entity)

            _cur.close()
        except(Exception) as e:
            self.add_log(str(e),type(self).__name__)
        finally:
            if _db is not None:
                _db.disconnect()
                print("Se cerro la conexion")
        return _data_row

    def update_user(self,userEntity):
        _db = None
        _id_user = 0
        _status = 1
        try:
            _db = Database()
            _db.connect(self.host,self.port,self.user,self.password,self.database)
            print('Se conecto a la bd')
            _con_client = _db.get_client()
            _sql = """UPDATE main.user_p SET  mail= %s, social_name= %s, full_name= %s, id_type_document= %s, document_number= %s, 
                      type_user= %s, photo= %s cellphone=%s, about=%s WHERE id = %s and status = %s;"""
            _cur = _con_client.cursor()
            _cur.execute(_sql, (userEntity.mail,userEntity.social_name,userEntity.full_name,
                                userEntity.id_type_document,userEntity.document_number,userEntity.type_user,
                                userEntity.photo,userEntity.cellphone,userEntity.about,userEntity.id,_status))
            _id_user = userEntity.id
            _con_client.commit()
            _cur.close()
        except(Exception) as e:
            self.add_log(str(e),type(self).__name__)
        finally:
            if _db is not None:
                _db.disconnect()
                print("Se cerro la conexion")
        return _id_user

    def validate_mail(self, mail):
        _db = None
        _value = False
        try:
            _mail = mail
            _db = Database()
            _db.connect(self.host,self.port,self.user,self.password,self.database)
            print('Se conecto a la bd')
            _con_client = _db.get_client()
            _sql = """SELECT id
                    FROM   main.user_p p 
                    WHERE p.mail = %s;"""   
            _cur = _con_client.cursor()
            _cur.execute(_sql,(_mail,))
            _rows = _cur.fetchall()
            if len(_rows) >= 1:
                _value = True
            _cur.close()
        except(Exception) as e:
            self.add_log(str(e),type(self).__name__)
        finally:
            if _db is not None:
                _db.disconnect()
                print("Se cerro la conexion")
        return _value

    def get_user_detail(self,id):
        _db = None
        _status = 1
        _data_services = []
        _data_rates = []
        _data_comments = []
        _id_user = id
        _userDetailEntity= None
        try:
            _userDetailEntity = userDetailEntity()
            _db = Database()
            _db.connect(self.host,self.port,self.user,self.password,self.database)
            print('Se conecto a la bd')
            _con_client = _db.get_client()
            
            _sql = """SELECT uss.id_service, 
                    s.full_name  AS service_name, 
                    us."enable"  AS service_enable, 
                    uss.id_sub_service, 
                    ss.full_name AS sub_service_name, 
                    uss.charge, 
                    uss."enable" AS sub_service_enable 
                FROM   main.user_sub_service uss 
                    INNER JOIN main.sub_service ss 
                            ON ss.id = uss.id_sub_service 
                    INNER JOIN main.service s 
                            ON uss.id_service = s.id 
                    INNER JOIN main.user_p up 
                            ON uss.id_user = up.id 
                    INNER JOIN main.user_service us 
                            ON us.id_service = s.id 
                WHERE  up.status = %s
                    AND uss."enable" = 1 
                    AND us."enable" = 1 
                    AND uss.id_user = %s 
                ORDER  BY 1; """
                                        
            _cur = _con_client.cursor()
            _cur.execute(_sql,(_status,_id_user,))
            _rows = _cur.fetchall()
            _id_service_old = None
            for row in _rows:
                _serviceEntity = serviceEntity()
                _serviceEntity.id  = row[0]
                _serviceEntity.full_name  = row[1] 
                _serviceEntity.enable  = row[2]
                _sub_services = []              
                if _id_service_old  != _serviceEntity.id :
                    for se in _rows:
                        if row[0] == se[0]:
                            _subServiceEntity = subServiceEntity()
                            _subServiceEntity.id = se[3]
                            _subServiceEntity.full_name = se[4]
                            _subServiceEntity.charge = se[5]
                            _subServiceEntity.enable = se[6]
                            _sub_services.append(_subServiceEntity)

                    _serviceEntity.sub_services = _sub_services
                    _data_services.append(_serviceEntity)
                    _id_service_old = _serviceEntity.id 

            _userDetailEntity.services = _data_services

            _sql_rate = """SELECT cr.rate, 
                        a.qua 						    AS total, 
                        Count(cr.id_user)               AS quantity, 
                        (Count(cr.id_user) * 1.0 / a.qua)::float4 AS percentage 
                    FROM   main.customer_rate cr 
                        INNER JOIN (SELECT id_user, 
                                            Count(id_user) AS qua 
                                    FROM   main.customer_rate 
                                    WHERE  id_user = %s
                                    GROUP  BY 1) a 
                                ON a.id_user = cr.id_user 
                    GROUP  BY 1, 2; """

            _cur.execute(_sql_rate,(_id_user,))
            _rows = _cur.fetchall()
            for row in _rows:
                _rateEntity = rateEntity()
                _rateEntity.rate = row[0]
                _rateEntity.total = row[1]
                _rateEntity.quantity = row[2]
                _rateEntity.percentage = row[3]
                _data_rates.append(_rateEntity)
            
            _userDetailEntity.rates = _data_rates

            _sql_comment = """ SELECT cr.rate, 
                    cr.description, 
                    To_char(cr.date_transaction, 'DD-MM-YYYY') AS date_transaction, 
                    c.full_name 
                FROM   main.customer_rate cr 
                    INNER JOIN main.customer c 
                            ON cr.id_customer = c.id 
                WHERE  id_user = %s
                ORDER BY cr.date_transaction desc
                LIMIT 10; """

            _cur.execute(_sql_comment,(_id_user,))
            _rows = _cur.fetchall()
            for row in _rows:
                _commentEntity = commentEntity()
                _commentEntity.rate = row[0]
                _commentEntity.description = row[1]
                _commentEntity.date_transaction = row[2]
                _commentEntity.full_name = row[3]
                _data_comments.append(_commentEntity)
            
            _userDetailEntity.comments = _data_comments

            _cur.close()
        except(Exception) as e:
            self.add_log(str(e),type(self).__name__)
        finally:
            if _db is not None:
                _db.disconnect()
                print("Se cerro la conexion")
        return _userDetailEntity