from flask import Flask, jsonify, request
from src.cn.data_base_connection import Database
from src.models.dbModel import dbModel
from src.entities.userEntity import userEntity

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
            print('error: '+ str(e))
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
            print('error: '+ str(e))
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
            print('error: '+ str(e))
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
            print('error: '+ str(e))
        finally:
            if _db is not None:
                _db.disconnect()
                print("Se cerro la conexion")
        return _entity

    def get_password_by_id(self,id):
        _db = None
        _status = 1
        _entity = None
        _id_user = id
        _password = None
        try:
            _db = Database()
            _db.connect(self.host,self.port,self.user,self.password,self.database)
            print('Se conecto a la bd')
            _con_client = _db.get_client()

            _sql = """SELECT up."password"
                    FROM   main.user_p up 
                    WHERE  up.status = %s
                        AND id = %s; """   

            _cur = _con_client.cursor()
            _cur.execute(_sql,(_status,_id_user,))
            _rows = _cur.fetchall()
        
            if len(_rows) >= 1:
                _password = _rows[0][0]

            _cur.close()
        except(Exception) as e:
            print('error: '+ str(e))
        finally:
            if _db is not None:
                _db.disconnect()
                print("Se cerro la conexion")
        return _password

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
            print('error: '+ str(e))
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
            print('error: '+ str(e))
        finally:
            if _db is not None:
                _db.disconnect()
                print("Se cerro la conexion")
        return _id_user
        