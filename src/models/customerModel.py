from flask import Flask, jsonify, request
from src.cn.data_base_connection import Database
from src.models.dbModel import dbModel
from src.entities.customerEntity import customerEntity
from src.entities.customeRateEntity import customerRateEntity

class customerModel(dbModel):

    def __init__(self):
        dbModel.__init__(self)

    def add_customer(self,entity):
        _db = None
        _id_customer = 0
        _status = 1
        _i = 0
        try:
            _db = Database()
            _db.connect(self.host,self.port,self.user,self.password,self.database)
            print('Se conecto a la bd')
            _con_client = _db.get_client()
            _sql = """INSERT INTO main.customer (mail,full_name,cellphone,photo,password,status) 
                    VALUES(%s,%s,%s,%s,%s,%s) RETURNING id;"""
            _cur = _con_client.cursor()
            _cur.execute(_sql, (entity.mail,entity.full_name,entity.cellphone,
                                entity.photo,entity.password,_status))
            _id_customer = _cur.fetchone()[0]
            entity.id = _id_customer
            
            _sql_store = """INSERT INTO main.customer_address(id_customer, address, longitude , latitude, main, status) 
                            VALUES(%s,%s,%s,%s,%s,%s) RETURNING id;"""
            for us in entity.customer_address:
                _cur.execute(_sql_store, (_id_customer,us.address,us.longitude,us.latitude,us.main,_status))
                _id_customer_address = _cur.fetchone()[0]
                entity.customer_address[_i].id = _id_customer_address
                entity.customer_address[_i].id_customer = _id_customer
                _i += 1

            _con_client.commit()
            _cur.close()
        except(Exception) as e:
            print('error: '+ str(e))
        finally:
            if _db is not None:
                _db.disconnect()
                print("Se cerro la conexion")
        return entity

    def add_customer_rate(self,entity):
        _db = None
        _id_customer = 0
        _status = 1
        _i = 0
        try:
            _db = Database()
            _db.connect(self.host,self.port,self.user,self.password,self.database)
            print('Se conecto a la bd')
            _con_client = _db.get_client()
            _sql = """INSERT INTO main.customer_rate (id_user,id_service,id_customer,rate,description,status) 
                    VALUES(%s,%s,%s,%s,%s,%s);"""
            _cur = _con_client.cursor()
            _cur.execute(_sql, (entity.id_user,entity.id_service,entity.id_customer,
                                entity.rate,entity.description,_status))
                                
            _con_client.commit()
            _cur.close()
        except(Exception) as e:
            print('error: '+ str(e))
        finally:
            if _db is not None:
                _db.disconnect()
                print("Se cerro la conexion")
        return entity

    def delete_customer(self,id):
        return None
    
    def get_customers(self):
        return None

    def get_customer_by_id(self,id):
        return None

    def update_customer(self,entity):
        return None
        