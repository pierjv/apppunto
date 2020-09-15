from flask import Flask, jsonify, request
from src.cn.data_base_connection import Database
from src.models.dbModel import dbModel
from src.entities.customerEntity import customerEntity,customerRateEntity, customerCouponEntity,customerAddressEntity, customerCardEntity
from datetime import datetime
from src.entities.serviceEntity import serviceEntity
from src.entities.subServiceEntity import subServiceEntity

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
            _sql = """INSERT INTO main.customer (mail,full_name,cellphone,photo,password,referred_code,status) 
                    VALUES(%s,%s,%s,%s,%s,%s,%s) RETURNING id;"""
            _cur = _con_client.cursor()
            _cur.execute(_sql, (entity.mail,entity.full_name,entity.cellphone,
                                entity.photo,entity.password,entity.referred_code,_status))
            _id_customer = _cur.fetchone()[0]
            entity.id = _id_customer

            _date = datetime.now()
            _id_code = "COD-APP"+ str(_id_customer) +"-"+ str(_date.hour)+str(_date.year)+str(_date.month)
            _sql_coupon = """UPDATE main.customer SET id_code = %s WHERE id = %s;"""
            _cur.execute(_sql_coupon,(_id_code,_id_customer))
            entity.id_code = _id_code

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
            _sql = """INSERT INTO main.customer_rate (id_user,id_service,id_customer,rate,description,status,date_transaction) 
                    VALUES(%s,%s,%s,%s,%s,%s,current_timestamp);"""
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

    def validate_referred_code(self, referred_coupon):
        _db = None
        _value = False
        _status = 1
        _id_customer = None
        try:
            _referred_coupon = referred_coupon
            _db = Database()
            _db.connect(self.host,self.port,self.user,self.password,self.database)
            print('Se conecto a la bd')
            _con_client = _db.get_client()
            _sql = """SELECT id
                    FROM   main.customer c 
                    WHERE c.id_code = %s AND c.status = %s;"""   
            _cur = _con_client.cursor()
            _cur.execute(_sql,(_referred_coupon,_status,))
            _rows = _cur.fetchall()
            if len(_rows) >= 1:
                _id_customer = _rows[0][0]
            _cur.close()
        except(Exception) as e:
            self.add_log(str(e),type(self).__name__)
        finally:
            if _db is not None:
                _db.disconnect()
                print("Se cerro la conexion")
        return _id_customer

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

    def add_customer_coupon(self,id_customer,id_customer_main):
        _db = None
        _id_customer = id_customer
        _id_customer_main = id_customer_main
        _status = 1
        _i = 0
        try:
            _db = Database()
            _db.connect(self.host,self.port,self.user,self.password,self.database)
            print('Se conecto a la bd')

            _date = datetime.now()
            entity = customerCouponEntity()
            entity.id_customer = _id_customer
            entity.coupon = "CON-APP"+ str(_id_customer) +"-"+ str(_date.hour)+str(_date.year)+str(_date.month)+str(_date.minute)
            entity.amount = int(self.amount_coupon)

            _con_client = _db.get_client()
            _sql = """INSERT INTO main.customer_coupon (coupon, id_customer, id_customer_main,effective_date, amount, status)
                    VALUES(%s,%s,%s,current_date + 30,%s,%s);"""
            _cur = _con_client.cursor()
            _cur.execute(_sql,(entity.coupon,entity.id_customer,_id_customer_main,entity.amount,_status))
                                
            _con_client.commit()
            _cur.close()
        except(Exception) as e:
            self.add_log(str(e),type(self).__name__)
        finally:
            if _db is not None:
                _db.disconnect()
                print("Se cerro la conexion")
        return entity
    
    def get_customer_coupon_by_id(self,id_customer):
        _db = None
        _status = 1
        _data_coupons = []
        _id_customer = id_customer
        try:
            _db = Database()
            _db.connect(self.host,self.port,self.user,self.password,self.database)
            print('Se conecto a la bd')
            _con_client = _db.get_client()

            _sql = """SELECT coupon, 
                    id_customer, 
                    To_char(effective_date, 'DD-MM-YYY') AS effective_date, 
                    amount 
                FROM   main.customer_coupon 
                WHERE  id_customer = %s 
                    AND status = %s; """   

            _cur = _con_client.cursor()
            _cur.execute(_sql,(_id_customer,_status,))
            _rows = _cur.fetchall()
        
            for row in _rows:
                _entity  = customerCouponEntity()
                _entity.coupon = row[0]
                _entity.id_customer = row[1]
                _entity.effective_date =row[2]
                _entity.amount =row[3]
                _data_coupons.append(_entity)

            _cur.close()
        except(Exception) as e:
            self.add_log(str(e),type(self).__name__)
        finally:
            if _db is not None:
                _db.disconnect()
                print("Se cerro la conexion")
        return _data_coupons

    def delete_customer(self,id):
        return None
    
    def get_customers(self):
        return None

    def get_customer_by_id(self,id):
        return None

    def update_customer(self,entity):
        return None
        
    def get_customer_address_by_id_customer(self,id_customer):
        _db = None
        _status = 1
        _data = []
        _id_customer = id_customer
        try:
            _db = Database()
            _db.connect(self.host,self.port,self.user,self.password,self.database)
            print('Se conecto a la bd')
            _con_client = _db.get_client()

            _sql = """SELECT id, 
                    id_customer, 
                    address, 
                    longitude, 
                    latitude, 
                    main 
                FROM   main.customer_address ca 
                WHERE  id_customer = %s 
                    AND status = %s; """   

            _cur = _con_client.cursor()
            _cur.execute(_sql,(_id_customer,_status,))
            _rows = _cur.fetchall()
        
            for row in _rows:
                _entity  = customerAddressEntity()
                _entity.id = row[0]
                _entity.id_customer = row[1]
                _entity.address =row[2]
                _entity.longitude =row[3]
                _entity.latitude =row[4]
                _entity.main =row[5]
                _data.append(_entity)

            _cur.close()
        except(Exception) as e:
            self.add_log(str(e),type(self).__name__)
        finally:
            if _db is not None:
                _db.disconnect()
                print("Se cerro la conexion")
        return _data

    def get_customer_card_by_id_customer(self,id_customer):
        _db = None
        _status = 1
        _data = []
        _id_customer = id_customer
        try:
            _db = Database()
            _db.connect(self.host,self.port,self.user,self.password,self.database)
            print('Se conecto a la bd')
            _con_client = _db.get_client()

            _sql = """SELECT cc.id, 
                    cc.id_customer,
                    id_type_card, 
                    document_number, 
                    expiration_year, 
                    expiration_month, 
                    email, 
                    full_name_card, 
                    tc.brand, 
                    tc.url_image 
                FROM   main.customer_card cc 
                    INNER JOIN main.type_card tc 
                            ON cc.id_type_card = tc.id 
                WHERE  cc.status = 1 
                    AND cc.id_customer = 3; """   

            _cur = _con_client.cursor()
            _cur.execute(_sql,(_id_customer,_status,))
            _rows = _cur.fetchall()
        
            for row in _rows:
                _entity  = customerCardEntity()
                _entity.id = row[0]
                _entity.id_customer = row[1]
                _entity.id_type_card = row[2]
                _entity.document_number =row[3]
                _entity.expiration_year =row[4]
                _entity.expiration_month =row[5]
                _entity.email =row[6]
                _entity.full_name_card =row[7]
                _entity.brand =row[8]
                _entity.url_image =row[9]
                _data.append(_entity)

            _cur.close()
        except(Exception) as e:
            self.add_log(str(e),type(self).__name__)
        finally:
            if _db is not None:
                _db.disconnect()
                print("Se cerro la conexion")
        return _data

    def add_customer_address(self,entity):
        _db = None
        _status = 1
        try:
            _db = Database()
            _db.connect(self.host,self.port,self.user,self.password,self.database)
            print('Se conecto a la bd')
            _con_client = _db.get_client()
            _sql = """INSERT INTO main.customer_address(id_customer, address, longitude , latitude, main, status) 
                            VALUES(%s,%s,%s,%s,%s,%s) RETURNING id;"""
            _cur = _con_client.cursor()
            _cur.execute(_sql, (entity.id_customer,entity.address,entity.longitude,entity.latitude,entity.main,_status))
            _id_customer = _cur.fetchone()[0]
            entity.id = _id_customer

            _con_client.commit()
            _cur.close()
        except(Exception) as e:
            self.add_log(str(e),type(self).__name__)
        finally:
            if _db is not None:
                _db.disconnect()
                print("Se cerro la conexion")
        return entity
    
    def update_customer_address(self,entity):
        _db = None
        _status = 1
        try:
            _db = Database()
            _db.connect(self.host,self.port,self.user,self.password,self.database)
            print('Se conecto a la bd')
            _con_client = _db.get_client()
            _sql = """UPDATE main.customer_address 
                    SET id_customer = %s,
                    address = %s,
                    longitude = %s,
                    latitude = %s,
                    main = %s
                    WHERE id = %s;"""

            _cur = _con_client.cursor()
            _cur.execute(_sql, (entity.id_customer,entity.address,entity.longitude,entity.latitude,entity.main,entity.id,))
            _con_client.commit()
            _cur.close()
        except(Exception) as e:
            self.add_log(str(e),type(self).__name__)
        finally:
            if _db is not None:
                _db.disconnect()
                print("Se cerro la conexion")
        return entity

    def delete_customer_address(self,id_customer_address):
        _db = None
        _status = 0
        try:
            _db = Database()
            _db.connect(self.host,self.port,self.user,self.password,self.database)
            print('Se conecto a la bd')
            _con_client = _db.get_client()
            _sql = """UPDATE main.customer_address 
                    SET status = %s
                    WHERE id = %s;"""

            _cur = _con_client.cursor()
            _cur.execute(_sql, (_status,id_customer_address,))
            _con_client.commit()
            _cur.close()
        except(Exception) as e:
            self.add_log(str(e),type(self).__name__)
        finally:
            if _db is not None:
                _db.disconnect()
                print("Se cerro la conexion")
        return id_customer_address

    def add_customer_card(self,entity):
        _db = None
        _status = 1
        try:
            _db = Database()
            _db.connect(self.host,self.port,self.user,self.password,self.database)
            print('Se conecto a la bd')
            _con_client = _db.get_client()
            _sql = """INSERT INTO main.customer_card (id_customer, id_type_card, document_number, expiration_year, expiration_month, email,full_name_card, status)
                            VALUES(%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id;"""
            _cur = _con_client.cursor()
            _cur.execute(_sql, (entity.id_customer,entity.id_type_card,entity.document_number,entity.expiration_year,entity.expiration_month,entity.email,entity.full_name_card, _status))
            _id_customer_card = _cur.fetchone()[0]
            entity.id = _id_customer_card

            _con_client.commit()
            _cur.close()
        except(Exception) as e:
            self.add_log(str(e),type(self).__name__)
        finally:
            if _db is not None:
                _db.disconnect()
                print("Se cerro la conexion")
        return entity

    def delete_customer_card(self,id_customer_card):
        _db = None
        _status = 0
        try:
            _db = Database()
            _db.connect(self.host,self.port,self.user,self.password,self.database)
            print('Se conecto a la bd')
            _con_client = _db.get_client()
            _sql = """UPDATE main.customer_card 
                    SET status = %s
                    WHERE id = %s;"""

            _cur = _con_client.cursor()
            _cur.execute(_sql, (_status,id_customer_card,))
            _con_client.commit()
            _cur.close()
        except(Exception) as e:
            self.add_log(str(e),type(self).__name__)
        finally:
            if _db is not None:
                _db.disconnect()
                print("Se cerro la conexion")
        return id_customer_card
    
    def get_id_fire_base_token_by_id_customer(self,id_customer):
        _db = None
        _status = 1
        _id_fire_base_token = None
        try:
            _id_customer = id_customer
            _db = Database()
            _db.connect(self.host,self.port,self.user,self.password,self.database)
            print('Se conecto a la bd')
            _con_client = _db.get_client()

            _sql = """SELECT c.id_fire_base_token
                    FROM   main.customer c 
                    WHERE c.id = %s;"""   

            _cur = _con_client.cursor()
            _cur.execute(_sql,(_id_customer,))
            _rows = _cur.fetchall()
        
            if len(_rows) >= 1:
                _id_fire_base_token = _rows[0][0]

            _cur.close()
        except(Exception) as e:
            self.add_log(str(e),type(self).__name__)
        finally:
            if _db is not None:
                _db.disconnect()
                print("Se cerro la conexion")
        return _id_fire_base_token
