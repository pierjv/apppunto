
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
            _sql = """SELECT id, full_name, color,encode(file_image,'base64') AS file_image FROM main.service WHERE status = 1 ORDER BY 1;"""
            _cur = _con_client.cursor()
            _cur.execute(_sql)
            _rows = _cur.fetchall()
            for row in _rows:
                _serviceEntity = serviceEntity()
                _serviceEntity.id  = row[0]
                _serviceEntity.full_name  = row[1] 
                _serviceEntity.color  = row[2] 
                _file_image = row[3]
                if _file_image is None:
                    _serviceEntity.file_image  = _file_image
                else:
                    _serviceEntity.file_image  = _file_image.replace('\n','')
                _data_row.append(_serviceEntity)

            _cur.close()
        except(Exception) as e:
            print('error: '+ str(e))
        finally:
            if _db is not None:
                _db.disconnect()
                print("Se cerro la conexion")
        return _data_row
    
    def get_services_wa(self):
        _db = None
        _status = 1
        _data_row = []
        try:
            _db = Database()
            _db.connect(self.host,self.port,self.user,self.password,self.database)
            print('Se conecto a la bd')
            _con_client = _db.get_client()
            _sql = """SELECT id, full_name, color,encode(file_image,'base64') AS file_image,status FROM main.service ORDER BY 1;"""
            _cur = _con_client.cursor()
            _cur.execute(_sql)
            _rows = _cur.fetchall()
            for row in _rows:
                _serviceEntity = serviceEntity()
                _serviceEntity.id  = row[0]
                _serviceEntity.full_name  = row[1] 
                _serviceEntity.color  = row[2] 
                _file_image = row[3]
                if _file_image is None:
                    _serviceEntity.file_image  = _file_image
                else:
                    _serviceEntity.file_image  = _file_image.replace('\n','')
                _serviceEntity.status = row[4]
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
                    s.color, 
                    Encode(s.file_image, 'base64') AS file_image, 
                    b.enable, 
                    ss.id                          AS id_sub_service, 
                    ss.full_name                   AS full_name_sub_service, 
                    c.charge, 
                    c."enable"                     AS enable_sub_service 
                FROM   main.service s 
                    LEFT JOIN (SELECT s.id AS id_service, 
                                        us.enable 
                                FROM   main.service s 
                                        LEFT JOIN main.user_service us 
                                                ON s.id = us.id_service 
                                WHERE  us.id_user = %s) b 
                            ON s.id = b.id_service 
                    LEFT JOIN main.sub_service ss 
                            ON s.id = ss.id_service 
                    LEFT JOIN (SELECT uss.id_service, 
                                        uss.id_sub_service, 
                                        uss.charge, 
                                        uss."enable" 
                                FROM   main.user_sub_service uss 
                                WHERE  uss.id_user = %s) c 
                            ON c.id_service = s.id 
                                AND c.id_sub_service = ss.id 
                ORDER  BY s.id; """
                                                    
            _cur = _con_client.cursor()
            _cur.execute(_sql,(_id_user,_id_user,))
            _rows = _cur.fetchall()

            _id_service_old = None
            for row in _rows:
                _serviceEntity = serviceEntity()
                _serviceEntity.id  = row[0]
                _serviceEntity.full_name  = row[1] 
                _serviceEntity.color  = row[2] 
                _file_image = row[3]
                if _file_image is None:
                    _serviceEntity.file_image  = _file_image
                else:
                    _serviceEntity.file_image  = _file_image.replace('\n','')
                _enable = row[4]
                if _enable is None:
                    _enable  = 0
                _serviceEntity.enable  = _enable
                _sub_service = row[5]
                _sub_services = []
                if _id_service_old  != _serviceEntity.id :
                    for se in _rows:
                        if row[0] == se[0] and _sub_service is not None:
                            _subServiceEntity = subServiceEntity()
                            _subServiceEntity.id = se[5]
                            _subServiceEntity.full_name = se[6]
                            _subServiceEntity.charge = se[7]
                            _enable_s = se[8]
                            if _enable_s is None:
                                _enable_s  = 0
                            _subServiceEntity.enable = _enable_s
                            _subServiceEntity.id_service = _serviceEntity.id 
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
                    WHERE  id = %s;"""
            _cur = _con_client.cursor()
            _cur.execute(_sql,(file_image,id_service,))
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
    
    def add_service(self,entity):
        _db = None
        _status = 1
        _i = 0
        try:
            _db = Database()
            _db.connect(self.host,self.port,self.user,self.password,self.database)
            print('Se conecto a la bd')

            _con_client = _db.get_client()
            _sql = """INSERT INTO main.service (full_name, status, color, file_image)
                    VALUES(%s,%s,%s,%s) RETURNING id;"""
            _cur = _con_client.cursor()
            _cur.execute(_sql,(entity.full_name,_status,entity.color,entity.file_image))
            _id_service = _cur.fetchone()[0]  
            entity.id = _id_service      
            _con_client.commit()
            _cur.close()
        except(Exception) as e:
            self.add_log(str(e),type(self).__name__)
        finally:
            if _db is not None:
                _db.disconnect()
                print("Se cerro la conexion")
        return entity
    
    def update_service(self,entity,status):
        _db = None
        _status = 1
        try:
            _db = Database()
            _db.connect(self.host,self.port,self.user,self.password,self.database)
            print('Se conecto a la bd')
            _con_client = _db.get_client()
            _sql = """UPDATE main.service 
                    SET    full_name = %s,
                    color = %s,
                    status = %s
                    WHERE  id = %s;"""
            _cur = _con_client.cursor()
            _cur.execute(_sql,(entity.full_name,entity.color,status,entity.id))
            _con_client.commit()
            _cur.close()
        except(Exception) as e:
            self.add_log(str(e),type(self).__name__)
        finally:
            if _db is not None:
                _db.disconnect()
                print("Se cerro la conexion")
        return entity

    def get_sub_services(self,id_service):
        _db = None
        _status = 1
        _data_row = []
        _id_service = id_service
        try:
            _db = Database()
            _db.connect(self.host,self.port,self.user,self.password,self.database)
            print('Se conecto a la bd')
            _con_client = _db.get_client()
            _sql = """SELECT ss.id, 
                    s.full_name  AS service, 
                    ss.full_name sub_service, 
                    ss.status, 
                    ss.in_filter 
                FROM   main.sub_service ss 
                    INNER JOIN main.service s 
                            ON ss.id_service = s.id 
                WHERE  ss.id_service = CASE 
                                        WHEN %s = 0 THEN ss.id_service 
                                        ELSE %s 
                                    END 
                ORDER  BY 1; """
            _cur = _con_client.cursor()
            _cur.execute(_sql,(_id_service,_id_service,))
            _rows = _cur.fetchall()
            for row in _rows:
                _entity = subServiceEntity()
                _entity.id  = row[0]
                _entity.service  = row[1]
                _entity.full_name  = row[2] 
                _entity.status  = row[3] 
                _entity.in_filter  = row[4]
                _data_row.append(_entity)

            _cur.close()
        except(Exception) as e:
            self.add_log(str(e),type(self).__name__)
        finally:
            if _db is not None:
                _db.disconnect()
                print("Se cerro la conexion")
        return _data_row
    
    def get_sub_services_by_id(self,id_sub_service):
        _db = None
        _id_sub_service = id_sub_service
        _entity = None
        try:
            _db = Database()
            _db.connect(self.host,self.port,self.user,self.password,self.database)
            print('Se conecto a la bd')
            _con_client = _db.get_client()
            _sql = """SELECT ss.id, 
                    ss.full_name AS sub_service, 
                    s.id         AS id_service, 
                    s.full_name  AS service, 
                    ss.status, 
                    ss.in_filter 
                FROM   main.sub_service ss 
                    INNER JOIN main.service s 
                            ON ss.id_service = s.id 
                WHERE  ss.id = %s;"""
            _cur = _con_client.cursor()
            _cur.execute(_sql,(_id_sub_service,))
            _rows = _cur.fetchall()
            
            if len(_rows) >= 1:
                _entity = subServiceEntity()
                _entity.id  = _rows[0][0]
                _entity.full_name  = _rows[0][1] 
                _entity.id_service  = _rows[0][2] 
                _entity.service  = _rows[0][3] 
                _entity.status  = _rows[0][4] 
                _entity.in_filter  = _rows[0][5]

            _cur.close()
        except(Exception) as e:
            self.add_log(str(e),type(self).__name__)
        finally:
            if _db is not None:
                _db.disconnect()
                print("Se cerro la conexion")
        return _entity

    def add_sub_service(self,entity,id_service,status):
        _db = None
        _status = status
        _id_service = id_service
        _i = 0
        try:
            _db = Database()
            _db.connect(self.host,self.port,self.user,self.password,self.database)
            print('Se conecto a la bd')

            _con_client = _db.get_client()
            _sql = """INSERT INTO main.sub_service (id_service, full_name, status, in_filter)
                    VALUES(%s,%s,%s,%s) RETURNING id;"""
            _cur = _con_client.cursor()
            _cur.execute(_sql,(_id_service,entity.full_name,_status,entity.in_filter,))
            _id_service = _cur.fetchone()[0]  
            entity.id = _id_service      
            _con_client.commit()
            _cur.close()
        except(Exception) as e:
            self.add_log(str(e),type(self).__name__)
        finally:
            if _db is not None:
                _db.disconnect()
                print("Se cerro la conexion")
        return entity
    
    def update_sub_service(self,entity,id_service,status):
        _db = None
        _status = 1
        try:
            _db = Database()
            _db.connect(self.host,self.port,self.user,self.password,self.database)
            print('Se conecto a la bd')
            _con_client = _db.get_client()
            _sql = """UPDATE main.sub_service 
                    SET    id_service = %s,
                    full_name = %s,
                    status = %s,
                    in_filter = %s
                    WHERE  id = %s;"""
            _cur = _con_client.cursor()
            _cur.execute(_sql,(id_service,entity.full_name,status,entity.in_filter,entity.id))
            _con_client.commit()
            _cur.close()
        except(Exception) as e:
            self.add_log(str(e),type(self).__name__)
        finally:
            if _db is not None:
                _db.disconnect()
                print("Se cerro la conexion")
        return entity
   
    def get_sub_services_by_id_service_and_id_user(self,id_service,id_user):
        _db = None
        _data = []
        try:
            _id_service = id_service
            _id_user = id_user
            _db = Database()
            _db.connect(self.host,self.port,self.user,self.password,self.database)
            print('Se conecto a la bd')
            _con_client = _db.get_client()
            _sql = """SELECT ss.id, 
                    ss.full_name, 
                    uss.charge, 
                    ss.id_service, 
                    uss.id_user 
                FROM   main.user_sub_service uss 
                    INNER JOIN main.sub_service ss 
                            ON uss.id_sub_service = ss.id 
                WHERE  uss.id_service = %s 
                    AND id_user = %s;"""
            _cur = _con_client.cursor()
            _cur.execute(_sql,(_id_service,_id_user,))
            _rows = _cur.fetchall()
            
            for row in _rows:
                _entity = subServiceEntity()
                _entity.id  = row[0]
                _entity.full_name  = row[1] 
                _entity.charge  = row[2] 
                _data.append(_entity)

            _cur.close()
        except(Exception) as e:
            self.add_log(str(e),type(self).__name__)
        finally:
            if _db is not None:
                _db.disconnect()
                print("Se cerro la conexion")
        return _data