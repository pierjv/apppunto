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
        try:
            _db = Database()
            _db.connect(self.host,self.port,self.user,self.password,self.database)
            print('Se conecto a la bd')
            _con_client = _db.get_client()
            _sql = """INSERT INTO main.user_p(mail,social_name,full_name,address,document_number,type_user,password,status)
                VALUES(%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id;"""
            _cur = _con_client.cursor()
            _cur.execute(_sql, (userEntity.mail,userEntity.social_name,userEntity.full_name,
                                userEntity.address,userEntity.document_number,userEntity.type_user,userEntity.password,_status))
            _id_user = _cur.fetchone()[0]
            print('id: ' + str(_id_user))
            _con_client.commit()
            _cur.close()
        except(Exception) as e:
            print('error: '+ str(e))
        finally:
            if _db is not None:
                _db.disconnect()
                print("Se cerro la conexion")
        return _id_user

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
            _sql = """SELECT id, mail, social_name, full_name, address, document_number, type_user, photo, status 
                      FROM main.user_p WHERE status = 1;"""
            _cur = _con_client.cursor()
            _cur.execute(_sql)
            _rows = _cur.fetchall()

            for row in _rows:
                _userEntity= userEntity()
                _userEntity.id  = row[0]
                _userEntity.mail  = row[1] 
                _userEntity.social_name  = row[2]
                _userEntity.full_name  = row[3]
                _userEntity.address  = row[4]
                _userEntity.document_number  = row[5]
                _userEntity.type_user  = row[6]
                _userEntity.photo  = row[7]
                _userEntity.status  = row[8]
                _data_row.append(_userEntity)

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
            _sql = """UPDATE main.user_p SET  mail= %s, social_name= %s, full_name= %s, address= %s, document_number= %s, 
                      type_user= %s, photo= %s WHERE id = %s and status = %s;"""
            _cur = _con_client.cursor()
            _cur.execute(_sql, (userEntity.mail,userEntity.social_name,userEntity.full_name,
                                userEntity.address,userEntity.document_number,userEntity.type_user,
                                userEntity.photo,userEntity.id,_status))
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
        