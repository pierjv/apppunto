from flask import Flask, jsonify, request
from src.cn.data_base_connection import Database
from src.models.dbModel import dbModel
from src.entities.customerEntity import customerEntity,customerRateEntity, customerCouponEntity,customerAddressEntity, customerCardEntity, customerUserFavoriteEntity
from datetime import datetime
from src.entities.serviceEntity import serviceEntity
from src.entities.subServiceEntity import subServiceEntity
from src.models.userModel import userModel

class customerModel(dbModel):

    def __init__(self):
        dbModel.__init__(self)

    def add_customer(self,entity):
        _db = None
        _id_customer = 0
        _status = 1
        _status_first_sale = 0
        _i = 0
        try:
            _db = Database()
            _db.connect(self.host,self.port,self.user,self.password,self.database)
            print('Se conecto a la bd')
            _con_client = _db.get_client()
            _sql = """INSERT INTO main.customer (mail,full_name,cellphone,photo,password,referred_code,status,status_first_sale) 
                    VALUES(%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id;"""
            _cur = _con_client.cursor()
            _cur.execute(_sql, (entity.mail,entity.full_name,entity.cellphone,
                                entity.photo,entity.password,entity.referred_code,_status,
                                _status_first_sale))
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

    def update_customer(self,customerEntity):
        _db = None
        _id_customer = 0
        _status = 1
        try:
            _db = Database()
            _db.connect(self.host,self.port,self.user,self.password,self.database)
            print('Se conecto a la bd')
            _con_client = _db.get_client()
            _sql = """UPDATE main.customer SET full_name= %s, cellphone= %s, photo= %s
                    WHERE id = %s and status = %s;"""
            _cur = _con_client.cursor()
            _cur.execute(_sql, (customerEntity.full_name,customerEntity.cellphone,
                                customerEntity.photo,customerEntity.id,
                                _status))
            _id_customer = customerEntity.id
            _con_client.commit()
            _cur.close()
        except(Exception) as e:
            self.add_log(str(e),type(self).__name__)
        finally:
            if _db is not None:
                _db.disconnect()
                print("Se cerro la conexion")
        return _id_customer

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
            _sql = """INSERT INTO main.customer_rate (id_user,id_sale,id_customer,rate,description,status,date_transaction) 
                    VALUES(%s,%s,%s,%s,%s,%s,current_timestamp);"""
            _cur = _con_client.cursor()
            _cur.execute(_sql, (entity.id_user,entity.id_sale,entity.id_customer,
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
        _userModel = None
        try:
            _db = Database()
            _db.connect(self.host,self.port,self.user,self.password,self.database)
            print('Se conecto a la bd')
            _userModel = userModel()

            _date = datetime.now()
            entity = customerCouponEntity()
            entity.id_customer = _id_customer
            entity.coupon = "CPN-APP"+ str(_id_customer) +"-"+ str(_date.hour)+str(_date.year)+str(_date.month)+str(_date.minute)
            entity.amount = int(self.amount_coupon)

            if (int(_userModel.get_coupon_status_wa()) == 1):
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
                WHERE  current_date <= effective_date
                    AND id_customer = %s 
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

    def delete_customer_coupon(self,coupon):
        _db = None
        _status = 0
        try:
            _db = Database()
            _db.connect(self.host,self.port,self.user,self.password,self.database)
            print('Se conecto a la bd')
            _con_client = _db.get_client()
            _sql = """UPDATE main.customer_coupon 
                    SET status = %s
                    WHERE coupon = %s;"""

            _cur = _con_client.cursor()
            _cur.execute(_sql, (_status,coupon,))
            _con_client.commit()
            _cur.close()
        except(Exception) as e:
            self.add_log(str(e),type(self).__name__)
        finally:
            if _db is not None:
                _db.disconnect()
                print("Se cerro la conexion")
        return coupon
    
    def get_customers(self):
        return None

    def get_customer_by_id(self,id):
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
                WHERE  cc.status = %s 
                    AND cc.id_customer = %s; """   

            _cur = _con_client.cursor()
            _cur.execute(_sql,(_status,_id_customer,))
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
    
    def update_customer_user_favorite(self,customerUserFavorite):
        _db = None
        _status = 1
        try:
            _db = Database()
            _db.connect(self.host,self.port,self.user,self.password,self.database)
            print('Se conecto a la bd')
            _con_client = _db.get_client()

            _sql = """SELECT c.id_user, c.id_customer, c."enable"
                    FROM   main.customer_user_favorite c 
                    WHERE c.id_user = %s and c.id_customer = %s;"""   

            _cur = _con_client.cursor()
            _cur.execute(_sql,(customerUserFavorite.id_user,customerUserFavorite.id_customer,))
            _rows = _cur.fetchall()
        
            if len(_rows) == 0 or _rows is None:
                _sql_add = """INSERT INTO main.customer_user_favorite (id_user, id_customer, "enable", status) 
                             VALUES(%s, %s, %s, %s);"""
                _cur.execute(_sql_add,(customerUserFavorite.id_user,customerUserFavorite.id_customer,customerUserFavorite.enable,_status,))
            else:
                _sql_update = """UPDATE main.customer_user_favorite SET "enable" = %s WHERE id_user = %s and id_customer = %s;"""
                _cur.execute(_sql_update,(customerUserFavorite.enable,customerUserFavorite.id_user,customerUserFavorite.id_customer,))


            _con_client.commit()
            _cur.close()
        except(Exception) as e:
            self.add_log(str(e),type(self).__name__)
        finally:
            if _db is not None:
                _db.disconnect()
                print("Se cerro la conexion")
        return customerUserFavorite


    def update_first_sale(self,id_customer):
        _db = None
        _status = 1
        try:
            _db = Database()
            _db.connect(self.host,self.port,self.user,self.password,self.database)
            print('Se conecto a la bd')
            _con_client = _db.get_client()
            _sql = """UPDATE main.customer 
                    SET status_first_sale = %s
                    WHERE id = %s;"""

            _cur = _con_client.cursor()
            _cur.execute(_sql, (_status,id_customer,))
            _con_client.commit()
            _cur.close()
        except(Exception) as e:
            self.add_log(str(e),type(self).__name__)
        finally:
            if _db is not None:
                _db.disconnect()
                print("Se cerro la conexion")
        return id_customer
    

    def get_quantity_first_sales(self,id_customer):
        _db = None
        _status = 1
        _referred_code = None
        _quantity = None
        _status_first_sale = 1
        try:
            _id_customer = id_customer
            _db = Database()
            _db.connect(self.host,self.port,self.user,self.password,self.database)
            print('Se conecto a la bd')
            _con_client = _db.get_client()
            _cur = _con_client.cursor()

            _sql = """SELECT s.referred_code
                    FROM   main.customer s 
                    WHERE s.id = %s; """   

            _cur.execute(_sql,(_id_customer,))
            _rows = _cur.fetchall()
            if len(_rows) >= 1:
                _referred_code = _rows[0][0]

            print(_referred_code)

            _sql_quantity = """SELECT count(*) as quantity 
                FROM   main.customer s 
                WHERE s.referred_code = %s and s.status_first_sale = %s; """   
            _cur.execute(_sql_quantity,(_referred_code,_status_first_sale,))
            _rows = _cur.fetchall()
            if len(_rows) >= 1:
                _quantity = _rows[0][0]
            print(_quantity)

            _cur.close()
        except(Exception) as e:
            self.add_log(str(e),type(self).__name__)
        finally:
            if _db is not None:
                _db.disconnect()
                print("Se cerro la conexion")
        return _quantity

    
    def update_first_sale_done(self,id_customer):
        _db = None
        _status_first_sale = 2
        _referred_code = None
        try:
            _id_customer = id_customer
            _db = Database()
            _db.connect(self.host,self.port,self.user,self.password,self.database)
            print('Se conecto a la bd')
            _con_client = _db.get_client()
            _cur = _con_client.cursor()

            _sql = """SELECT s.referred_code
                    FROM   main.customer s 
                    WHERE s.id = %s; """   

 
            _cur.execute(_sql,(_id_customer,))
            _rows = _cur.fetchall()
        
            if len(_rows) >= 1:
                _referred_code = _rows[0][0]

            _sql_update = """UPDATE main.customer 
                    SET status_first_sale = %s
                    WHERE referred_code = %s and status_first_sale = 1;"""

            _cur = _con_client.cursor()
            _cur.execute(_sql_update, (_status_first_sale,_referred_code,))
            _con_client.commit()
            _cur.close()
        except(Exception) as e:
            self.add_log(str(e),type(self).__name__)
        finally:
            if _db is not None:
                _db.disconnect()
                print("Se cerro la conexion")
        return id_customer

    def get_id_customer_main_referred(self,id_customer):
        _db = None
        _status = 1
        _referred_code = None
        _id_customer_main = None
        try:
            _id_customer = id_customer
            _db = Database()
            _db.connect(self.host,self.port,self.user,self.password,self.database)
            print('Se conecto a la bd')
            _con_client = _db.get_client()
            _cur = _con_client.cursor()

            _sql = """SELECT s.referred_code
                    FROM   main.customer s 
                    WHERE s.id = %s; """   

            _cur.execute(_sql,(_id_customer,))
            _rows = _cur.fetchall()
            if len(_rows) >= 1:
                _referred_code = _rows[0][0]

            _sql_quantity = """SELECT s.id
                FROM   main.customer s 
                WHERE s.id_code = %s; """   
            _cur.execute(_sql_quantity,(_referred_code,))
            _rows = _cur.fetchall()
            if len(_rows) >= 1:
                _id_customer_main = _rows[0][0]

            _cur.close()
        except(Exception) as e:
            self.add_log(str(e),type(self).__name__)
        finally:
            if _db is not None:
                _db.disconnect()
                print("Se cerro la conexion")
        return _id_customer_main

    def get_cellphone_by_id(self,id_customer):
        _db = None
        _status = 1
        _cellphone = None
        try:
            _id_customer = id_customer
            _db = Database()
            _db.connect(self.host,self.port,self.user,self.password,self.database)
            print('Se conecto a la bd')
            _con_client = _db.get_client()
            _cur = _con_client.cursor()

            _sql = """SELECT s.cellphone
                    FROM   main.customer s 
                    WHERE s.id = %s; """   

            _cur.execute(_sql,(_id_customer,))
            _rows = _cur.fetchall()
            if len(_rows) >= 1:
                _cellphone = _rows[0][0]

            _cur.close()
        except(Exception) as e:
            self.add_log(str(e),type(self).__name__)
        finally:
            if _db is not None:
                _db.disconnect()
                print("Se cerro la conexion")
        return _cellphone
