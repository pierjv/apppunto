
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
            _sql = """SELECT id, full_name, url_image, status FROM main.service
                      WHERE status = %s;"""
            _cur = _con_client.cursor()
            _cur.execute(_sql,(_status,))
            _rows = _cur.fetchall()
            for row in _rows:
                _serviceEntity = serviceEntity()
                _serviceEntity.id  = row[0]
                _serviceEntity.full_name  = row[1] 
                _serviceEntity.url_image  = row[2]
                _serviceEntity.status  = row[3]
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
                        s.url_image, 
                        b.enable, 
                        s.status 
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
                _serviceEntity.url_image  = row[2]
                _serviceEntity.enable  = row[3]
                _data_row.append(_serviceEntity)

            _cur.close()
        except(Exception) as e:
            print('error: '+ str(e))
        finally:
            if _db is not None:
                _db.disconnect()
                print("Se cerro la conexion")
        return _data_row

    def get_services_load(self):
        _db = None
        _status = 1
        _data_row = []
        try:
            _db = Database()
            _db.connect(self.host,self.port,self.user,self.password,self.database)
            print('Se conecto a la bd')
            _con_client = _db.get_client()
            _sql = """SELECT s.id, 
                        s.full_name, 
                        s.url_image,
                        s.color, 
                        ss.id        AS id_sub_service, 
                        ss.full_name AS sub_service_name 
                    FROM   main.service s 
                        LEFT JOIN main.sub_service ss 
                                ON s.id = ss.id_service 
                    ORDER  BY 1;"""
                                        
            _cur = _con_client.cursor()
            _cur.execute(_sql)
            _rows = _cur.fetchall()
            _id_service_old = None
            for row in _rows:
                _serviceEntity = serviceEntity()
                _serviceEntity.id  = row[0]
                _serviceEntity.full_name  = row[1] 
                _serviceEntity.url_image  = row[2]
                _serviceEntity.color  = row[3]
                _sub_service = row[4]
                _sub_services = []
                if _id_service_old  != _serviceEntity.id :
                    for se in _rows:
                        if row[0] == se[0] and _sub_service is not None:
                            _subServiceEntity = subServiceEntity()
                            _subServiceEntity.id = se[4]
                            _subServiceEntity.full_name = se[5]
                            _sub_services.append(_subServiceEntity)

                    _serviceEntity.sub_services = _sub_services
                    _data_row.append(_serviceEntity)
                    _id_service_old = _serviceEntity.id 

            _cur.close()
        except(Exception) as e:
            print('error: '+ str(e))
        finally:
            if _db is not None:
                _db.disconnect()
                print("Se cerro la conexion")
        return _data_row
    
    def get_sub_services_by_id_user(self,id):
        _db = None
        _status = 1
        _data_row = []
        _id_user = id
        try:
            _db = Database()
            _db.connect(self.host,self.port,self.user,self.password,self.database)
            print('Se conecto a la bd')
            _con_client = _db.get_client()
            _sql = """SELECT uss.id_service, 
                    s.full_name  AS service_name, 
                    s.url_image, 
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
                WHERE  up.status = 1 
                    AND uss."enable" = 1 
                    AND us."enable" = 1 
                    AND uss.id_user = 26 
                ORDER  BY 1; """
                                        
            _cur = _con_client.cursor()
            _cur.execute(_sql,(_status,_id_user,))
            _rows = _cur.fetchall()
            _id_service_old = None
            for row in _rows:
                _serviceEntity = serviceEntity()
                _serviceEntity.id  = row[0]
                _serviceEntity.full_name  = row[1] 
                _serviceEntity.url_image  = row[2]
                _serviceEntity.enable  = row[3]
                _sub_services = []              
                if _id_service_old  != _serviceEntity.id :
                    for se in _rows:
                        if row[0] == se[0]:
                            _subServiceEntity = subServiceEntity()
                            _subServiceEntity.id = se[4]
                            _subServiceEntity.full_name = se[5]
                            _subServiceEntity.charge = se[6]
                            _subServiceEntity.enable = se[7]
                            _sub_services.append(_subServiceEntity)

                    _serviceEntity.sub_services = _sub_services
                    _data_row.append(_serviceEntity)
                    _id_service_old = _serviceEntity.id 

            _cur.close()
        except(Exception) as e:
            print('error: '+ str(e))
        finally:
            if _db is not None:
                _db.disconnect()
                print("Se cerro la conexion")
        return _data_row