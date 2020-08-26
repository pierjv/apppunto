from flask import Flask, jsonify, request
from src.cn.data_base_connection import Database
from src.models.dbModel import dbModel
from src.entities.customerEntity import customerEntity,customerRateEntity
from datetime import datetime

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
            _sql = """INSERT INTO main.customer (mail,full_name,cellphone,photo,password,referred_coupon,status) 
                    VALUES(%s,%s,%s,%s,%s,%s,%s) RETURNING id;"""
            _cur = _con_client.cursor()
            _cur.execute(_sql, (entity.mail,entity.full_name,entity.cellphone,
                                entity.photo,entity.password,entity.referred_coupon,_status))
            _id_customer = _cur.fetchone()[0]
            entity.id = _id_customer

            _date = datetime.now()
            _coupon = "CPN-APP"+ str(_id_customer) +"-"+ str(_date.hour)+str(_date.year)+str(_date.month)
            _sql_coupon = """UPDATE main.customer SET coupon = %s WHERE id = %s;"""
            _cur.execute(_sql_coupon,(_coupon,_id_customer))
            entity.coupon = _coupon

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
            self.add_log(str(e),type(self).__name__)
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
            self.add_log(str(e),type(self).__name__)
        finally:
            if _db is not None:
                _db.disconnect()
                print("Se cerro la conexion")
        return entity

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
                    FROM   main.customer c 
                    WHERE c.mail = %s;"""   
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

    def validate_referred_coupon(self, referred_coupon):
        _db = None
        _value = False
        _status = 1
        try:
            _referred_coupon = referred_coupon
            _db = Database()
            _db.connect(self.host,self.port,self.user,self.password,self.database)
            print('Se conecto a la bd')
            _con_client = _db.get_client()
            _sql = """SELECT id
                    FROM   main.customer c 
                    WHERE c.coupon = %s AND c.status = %s;"""   
            _cur = _con_client.cursor()
            _cur.execute(_sql,(_referred_coupon,_status,))
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

            _sql = """SELECT c."password", c.cellphone
                    FROM   main.customer c 
                    WHERE  c.status = %s
                        AND c.mail = %s; """   

            _cur = _con_client.cursor()
            _cur.execute(_sql,(_status,_mail,))
            _rows = _cur.fetchall()
        
            if len(_rows) >= 1:
                _entity  = customerEntity()
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

    def delete_customer(self,id):
        return None
    
    def get_customers(self):
        return None

    def get_customer_by_id(self,id):
        return None

    def update_customer(self,entity):
        return None
        