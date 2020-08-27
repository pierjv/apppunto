
from flask import Flask, jsonify, request
from src.cn.data_base_connection import Database
from src.models.dbModel import dbModel
from src.entities.serviceEntity import serviceEntity
from src.entities.subServiceEntity import subServiceEntity

class serviceModel(dbModel):

    def __init__(self):
        dbModel.__init__(self)

    def get_services(self):
        _db = None
        _status = 1
        _data_row = []
        try:
            _db = Database()
            _db.connect(self.host,self.port,self.user,self.password,self.database)
            print('Se conecto a la bd')
            _con_client = _db.get_client()
            _sql = """SELECT id, full_name, color, status,encode(file_image,'base64') AS file_image FROM main.service;"""
            _cur = _con_client.cursor()
            _cur.execute(_sql)
            _rows = _cur.fetchall()
            for row in _rows:
                _serviceEntity = serviceEntity()
                _serviceEntity.id  = row[0]
                _serviceEntity.full_name  = row[1] 
                _serviceEntity.color  = row[2] 
                _serviceEntity.status  = row[3]
                _serviceEntity.file_image  = row[4].replace('\n','') 
                _data_row.append(_serviceEntity)

            _cur.close()
        except(Exception) as e:
            print('error: '+ str(e))
        finally:
            if _db is not None:
                _db.disconnect()
                print("Se cerro la conexion")
        return _data_row

    def get_services_by_user(self,id_user):
        _db = None
        _status = 1
        _data_row = []
        _id_user = id_user
        try:
            _db = Database()
            _db.connect(self.host,self.port,self.user,self.password,self.database)
            print('Se conecto a la bd')
            _con_client = _db.get_client()
            _sql = """SELECT s.id, 
                        s.full_name, 
                        b.enable
                    FROM   main.service s 
                        LEFT JOIN (SELECT s.id AS id_service, 
                                            us.enable 
                                    FROM   main.service s 
                                            LEFT JOIN main.user_service us 
                                                    ON s.id = us.id_service 
                                    WHERE  us.id_user = %s) b 
                                ON s.id = b.id_service; """
                                        
            _cur = _con_client.cursor()
            _cur.execute(_sql,(_id_user,))
            _rows = _cur.fetchall()
            for row in _rows:
                _serviceEntity = serviceEntity()
                _serviceEntity.id  = row[0]
                _serviceEntity.full_name  = row[1] 
                _serviceEntity.enable  = row[2]
                _data_row.append(_serviceEntity)

            _cur.close()
        except(Exception) as e:
            print('error: '+ str(e))
        finally:
            if _db is not None:
                _db.disconnect()
                print("Se cerro la conexion")
        return _data_row
    
    def update_file_image(self,id_service,file_image):
        _db = None
        _status = 1
        _data_row = []
        try:
            _db = Database()
            _db.connect(self.host,self.port,self.user,self.password,self.database)
            print('Se conecto a la bd')
            _con_client = _db.get_client()
            _sql = """UPDATE main.service 
                    SET    file_image = %s 
                    WHERE  id = %s and status = %s;"""
            _cur = _con_client.cursor()
            _cur.execute(_sql,(file_image,id_service,_status,))
            _con_client.commit()
            _cur.close()
        except(Exception) as e:
            print('error: '+ str(e))
        finally:
            if _db is not None:
                _db.disconnect()
                print("Se cerro la conexion")
        return _data_row
    
    def get_services_by_id(self,id_service):
        _db = None
        _status = 1
        _id_service = id_service
        _entity = None
        try:
            _db = Database()
            _db.connect(self.host,self.port,self.user,self.password,self.database)
            print('Se conecto a la bd')
            _con_client = _db.get_client()
            _sql = """SELECT id, 
                    full_name, 
                    color, 
                    status, 
                    Encode(file_image, 'base64') AS file_image 
                FROM   main.service 
                WHERE  id = %s;"""
            _cur = _con_client.cursor()
            _cur.execute(_sql,(_id_service,))
            _rows = _cur.fetchall()
            
            if len(_rows) >= 1:
                _entity = serviceEntity()
                _entity.id  = _rows[0][0]
                _entity.full_name  = _rows[0][1] 
                _entity.color  = _rows[0][2] 
                _entity.status  = _rows[0][3]
                _entity.file_image  = _rows[0][4].replace('\n','') 

            _cur.close()
        except(Exception) as e:
            print('error: '+ str(e))
        finally:
            if _db is not None:
                _db.disconnect()
                print("Se cerro la conexion")
        return _entity