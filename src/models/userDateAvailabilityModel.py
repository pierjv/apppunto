
from flask import Flask, jsonify, request
from src.cn.data_base_connection import Database
from src.models.dbModel import dbModel
from src.entities.userDateAvailabilityEntity import userDateAvailabilityEntity,userDateAndHourAvailabilityEntity

class userDateAvailabilityModel(dbModel):

    def __init__(self):
        dbModel.__init__(self)

    def get_user_date_availability_by_user(self,id_user):
        _db = None
        _status = 1
        _data_row = []
        _id_user = id_user
        try:
            _db = Database()
            _db.connect(self.host,self.port,self.user,self.password,self.database)
            print('Se conecto a la bd')
            _con_client = _db.get_client()
            _sql = """SELECT ud.id_user, 
                        ud.id_type_availability, 
                        ta.full_name, 
                        to_char(ud.date_availability,'DD-MM-YYYY') as date_availability, 
                        ud.hour_availability, 
                        ud."enable"
                    FROM   main.user_date_availability ud 
                        INNER JOIN main.type_availability ta 
                                ON ud.id_type_availability = ta.id 
                    WHERE  ud.status = %s and ud.id_user = %s and ud."enable" = 1
                    order by 4,5; """
                                        
            _cur = _con_client.cursor()
            _cur.execute(_sql,(_status,_id_user,))
            _rows = _cur.fetchall()
            _id_date_old = None
            for row in _rows:
                _entity = userDateAndHourAvailabilityEntity()
                _entity.id_user  = row[0]
                _entity.id_type_availability  = row[1] 
                _entity.full_name  = row[2] 
                _entity.date_availability  = row[3] 
                _entity.enable  = row[5]
                _hours = []
                if _id_date_old  != _entity.date_availability :
                    for se in _rows:
                        if row[3] == se[3]:
                            _hours.append(se[4])

                    _entity.hours_availability = _hours
                    _data_row.append(_entity)
                    _id_date_old = _entity.date_availability 

            _cur.close()
        except(Exception) as e:
            self.add_log(str(e),type(self).__name__)
        finally:
            if _db is not None:
                _db.disconnect()
                print("Se cerro la conexion")
        return _data_row

    def update_user_date_availability(self,entity):
        _db = None
        _status = 1
        _i = 0
        _data_row = []
        try:
            _db = Database()
            _db.connect(self.host,self.port,self.user,self.password,self.database)
            _entities = entity.user_date_availabilities
            print('Se conecto a la bd')
            _con_client = _db.get_client()
            _cur = _con_client.cursor()

            _sql_delete = """DELETE FROM main.user_date_availability 
                            WHERE  id_user = %s 
                                AND id_type_availability = %s
                                AND date_availability = To_date(%s, 'DD-MM-YYYY') 
                                AND hour_availability = %s; """
            
            _sql_insert = """INSERT INTO main.user_date_availability
                                (id_user, id_type_availability, date_availability, hour_availability, enable, status) 
                                VALUES(%s, %s,to_date(%s,'DD-MM-YYYY') , %s, %s, %s) RETURNING status;"""

            for us in _entities:
                _cur.execute(_sql_delete, (us.id_user,us.id_type_availability,us.date_availability,us.hour_availability,))
                _cur.execute(_sql_insert, (us.id_user,us.id_type_availability,us.date_availability,us.hour_availability,us.enable,_status,))
                _status_insert = _cur.fetchone()[0]
                _entities[_i].status = _status_insert
                _data_row.append(_entities[_i])
                _i += 1
  

            _con_client.commit()
            _cur.close()
        except(Exception) as e:
            self.add_log(str(e),type(self).__name__)
        finally:
            if _db is not None:
                _db.disconnect()
                print("Se cerro la conexion")
        return _data_row