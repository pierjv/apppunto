from flask import Flask, jsonify, request
from src.cn.data_base_connection import Database
from src.models.dbModel import dbModel
from src.entities.userEntity import userEntity
from src.entities.userStoreEntity import userStoreEntity

class userStoreModel(dbModel):

    def __init__(self):
        dbModel.__init__(self)

    def get_user_stores_by_id_user(self,id_user):
        _db = None
        _status = 1
        _id_user = id_user
        _data_row = []
        print(id_user)
        try:
            _db = Database()
            _db.connect(self.host,self.port,self.user,self.password,self.database)
            print('Se conecto a la bd')
            _con_client = _db.get_client()
            _sql = """SELECT id, id_user, full_name, address, longitude, latitude, main, status FROM main.user_store
                      WHERE status = %s and id_user = %s;"""
            _cur = _con_client.cursor()
            _cur.execute(_sql,(_status,_id_user))
            _rows = _cur.fetchall()

            for row in _rows:
                _userStoreEntity= userStoreEntity()
                _userStoreEntity.id  = row[0]
                _userStoreEntity.id_user  = row[1] 
                _userStoreEntity.full_name  = row[2]
                _userStoreEntity.address  = row[3]
                _userStoreEntity.longitude  = row[4]
                _userStoreEntity.latitude  = row[5]
                _userStoreEntity.main  = row[6]
                _data_row.append(_userStoreEntity)
            _cur.close()
        except(Exception) as e:
            self.add_log(str(e),type(self).__name__)
        finally:
            if _db is not None:
                _db.disconnect()
                print("Se cerro la conexion")
        return _data_row
    
    def add_user_store(self,entity):
        _db = None
        _id = 0
        _status = 1
        _i = 0
        try:
            _db = Database()
            _db.connect(self.host,self.port,self.user,self.password,self.database)
            print('Se conecto a la bd')
            _con_client = _db.get_client()
            _sql = """INSERT INTO main.user_store (id_user,full_name, address, longitude, latitude, main, status ) 
                    VALUES(%s,%s,%s,%s,%s,%s,%s) RETURNING id;"""
            _cur = _con_client.cursor()
            _cur.execute(_sql, (entity.id_user,entity.full_name,entity.address,
                                entity.longitude,entity.latitude,entity.main,_status))
            _id = _cur.fetchone()[0]
            entity.id = _id
                                
            _con_client.commit()
            _cur.close()
        except(Exception) as e:
            self.add_log(str(e),type(self).__name__)
        finally:
            if _db is not None:
                _db.disconnect()
                print("Se cerro la conexion")
        return entity

    def delete_user_store(self,id_user_store):
        _db = None
        _status = 0
        try:
            _db = Database()
            _db.connect(self.host,self.port,self.user,self.password,self.database)
            print('Se conecto a la bd')
            _con_client = _db.get_client()
            _sql = """UPDATE main.user_store 
                    SET status = %s
                    WHERE id = %s;"""

            _cur = _con_client.cursor()
            _cur.execute(_sql, (_status,id_user_store,))
            _con_client.commit()
            _cur.close()
        except(Exception) as e:
            self.add_log(str(e),type(self).__name__)
        finally:
            if _db is not None:
                _db.disconnect()
                print("Se cerro la conexion")
        return id_user_store