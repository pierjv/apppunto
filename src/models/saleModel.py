
from flask import Flask, jsonify, request
from src.cn.data_base_connection import Database
from src.models.dbModel import dbModel
from src.entities.serviceEntity import serviceEntity
from src.entities.subServiceEntity import subServiceEntity
from src.entities.saleEntity import saleEntity,saleResponseEntity, typeSaleResponseEntity

class saleModel(dbModel):

    def __init__(self):
        dbModel.__init__(self)

    def add_sale_reserve(self,saleEntity):

        _db = None
        _id_user = 0
        _status = 1
        _status_sale = 0
        _i = 0
        try:
            _db = Database()
            _db.connect(self.host,self.port,self.user,self.password,self.database)
            print('Se conecto a la bd')
            _con_client = _db.get_client()
            _sql = """INSERT INTO main.sale (id_type_availability, id_customer, id_user, coupon, date_availability, hour_availability, total_amount,
                      status, date_transaction,id_type_card, document_number,expiration_year,expiration_month,mail,full_name_card,id_customer_address,status_sale)
                      VALUES(%s,%s,%s,%s,to_date(%s,'DD-MM-YYY'),%s,%s,%s,current_timestamp,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id;"""
            _cur = _con_client.cursor()
            _cur.execute(_sql, (saleEntity.id_type_availability,saleEntity.id_customer,saleEntity.id_user,
                                saleEntity.coupon,saleEntity.date_availability,saleEntity.hour_availability,
                                saleEntity.total_amount,_status,saleEntity.id_type_card,
                                saleEntity.document_number,saleEntity.expiration_year,saleEntity.expiration_month,
                                saleEntity.mail,saleEntity.full_name_card,saleEntity.id_customer_address,_status_sale))
            _id_sale = _cur.fetchone()[0]
            saleEntity.id = _id_sale
            
            _sql_store = """INSERT INTO main.type_sale (id_sale, id_sub_service, amount, status,date_transaction) 
                            VALUES(%s,%s,%s,%s,current_timestamp) RETURNING id;"""
            for us in saleEntity.type_sales:
                _cur.execute(_sql_store, (_id_sale,us.id_sub_service,us.amount,_status))
                _id_type_sale = _cur.fetchone()[0]
                saleEntity.type_sales[_i].id = _id_type_sale
                saleEntity.type_sales[_i].id_sale = _id_sale
                _i += 1

            _con_client.commit()
            _cur.close()
        except(Exception) as e:
            self.add_log(str(e),type(self).__name__)
        finally:
            if _db is not None:
                _db.disconnect()
                print("Se cerro la conexion")
        return saleEntity

    def add_sale_confirm(self,id_sale):
        _db = None
        _status_sale = 1
        try:
            _db = Database()
            _db.connect(self.host,self.port,self.user,self.password,self.database)
            print('Se conecto a la bd')
            _con_client = _db.get_client()
            _sql = """UPDATE main.sale 
                    SET status_sale = %s
                    WHERE id = %s;"""

            _cur = _con_client.cursor()
            _cur.execute(_sql, (_status_sale,id_sale,))
            _con_client.commit()
            _cur.close()
        except(Exception) as e:
            self.add_log(str(e),type(self).__name__)
        finally:
            if _db is not None:
                _db.disconnect()
                print("Se cerro la conexion")
        return id_sale

    def get_sale_by_id_sale(self,id_sale):
        _db = None
        _status = 1
        _data = None
        try:
            _id_sale = id_sale
            _db = Database()
            _db.connect(self.host,self.port,self.user,self.password,self.database)
            print('Se conecto a la bd')
            _con_client = _db.get_client()
            _sql = """SELECT s.id, 
                        id_type_availability, 
                        ta.full_name  as full_name_id_type_availability,
                        s.id_customer, 
                        id_user, 
                        coupon, 
                        to_char(date_availability,'DD-MM-YYYY') as date_availability, 
                        hour_availability, 
                        total_amount,  
                        id_type_card, 
                        document_number, 
                        expiration_year, 
                        expiration_month, 
                        mail, 
                        full_name_card, 
                        status_sale, 
                        ts.id        AS id_type_sale, 
                        ts.amount 	as amount_type_sale,
                        ts.id_sub_service, 
                        ss.full_name AS full_name_sub_service,
                        s.id_customer_address ,
                        ca.address 
                    FROM   main.sale s 
                        INNER JOIN main.type_sale ts 
                                ON s.id = ts.id_sale 
                        INNER JOIN main.sub_service ss 
                                ON ss.id = ts.id_sub_service 
                        INNER JOIN main.type_availability ta
       			                ON ta.id  = s.id_type_availability
                        INNER JOIN main.customer_address ca 
       			                ON ca.id  = s.id_customer_address  
                    WHERE  s.id = %s 
                        AND s.status = %s; """
                                        
            _cur = _con_client.cursor()
            _cur.execute(_sql,(_id_sale,_status))
            _rows = _cur.fetchall()
            _id_old = None
            for row in _rows:
                _entity = saleResponseEntity()
                _entity.id  = row[0]
                _entity.id_type_availability  = row[1] 
                _entity.full_name_type_availability  = row[2]
                _entity.id_customer  = row[3]
                _entity.id_user  = row[4]
                _entity.coupon = row[5]
                _entity.date_availability  = row[6]
                _entity.hour_availability  = row[7] 
                _entity.total_amount  = row[8]
                _entity.id_type_card  = row[9]
                _entity.document_number = row[10]
                _entity.expiration_year  = row[11]
                _entity.expiration_month  = row[12] 
                _entity.mail  = row[13]
                _entity.full_name_card  = row[14]
                _entity.status_sale = row[15]
                _entity.id_customer_address = row[20]
                _entity.address = row[21]
                
                _type_sales = []
                if _id_old  != _entity.id :
                    for se in _rows:
                        if row[0] == se[0]:
                            _typeSaleResponseEntity = typeSaleResponseEntity()
                            _typeSaleResponseEntity.id = se[16]
                            _typeSaleResponseEntity.amount = se[17]
                            _typeSaleResponseEntity.id_sub_service = se[18]
                            _typeSaleResponseEntity.full_name = se[19]
                            _typeSaleResponseEntity.id_sale = _entity.id
                            _type_sales.append(_typeSaleResponseEntity)

                    _entity.type_sales = _type_sales
                    _id_old = _entity.id 
                    _data = _entity

            _cur.close()
        except(Exception) as e:
            self.add_log(str(e),type(self).__name__)
        finally:
            if _db is not None:
                _db.disconnect()
                print("Se cerro la conexion")
        return _data

    def get_sale_by_id_customer(self,id_customer):
        _db = None
        _status = 1
        _data = []
        try:
            _id_customer = id_customer
            _db = Database()
            _db.connect(self.host,self.port,self.user,self.password,self.database)
            print('Se conecto a la bd')
            _con_client = _db.get_client()
            _sql = """SELECT s.id, 
                        id_type_availability, 
                        ta.full_name  as full_name_id_type_availability,
                        s.id_customer, 
                        id_user, 
                        coupon, 
                        to_char(date_availability,'DD-MM-YYYY') as date_availability, 
                        hour_availability, 
                        total_amount,  
                        id_type_card, 
                        document_number, 
                        expiration_year, 
                        expiration_month, 
                        mail, 
                        full_name_card, 
                        status_sale, 
                        ts.id        AS id_type_sale, 
                        ts.amount 	as amount_type_sale,
                        ts.id_sub_service, 
                        ss.full_name AS full_name_sub_service,
                        s.id_customer_address ,
                        ca.address 
                    FROM   main.sale s 
                        INNER JOIN main.type_sale ts 
                                ON s.id = ts.id_sale 
                        INNER JOIN main.sub_service ss 
                                ON ss.id = ts.id_sub_service 
                        INNER JOIN main.type_availability ta
       			                ON ta.id  = s.id_type_availability
                        INNER JOIN main.customer_address ca 
       			                ON ca.id  = s.id_customer_address  
                    WHERE  s.id_customer = %s 
                        AND s.status = %s; """
                                        
            _cur = _con_client.cursor()
            _cur.execute(_sql,(_id_customer,_status))
            _rows = _cur.fetchall()
            _id_old = None
            for row in _rows:
                _entity = saleResponseEntity()
                _entity.id  = row[0]
                _entity.id_type_availability  = row[1] 
                _entity.full_name_type_availability  = row[2]
                _entity.id_customer  = row[3]
                _entity.id_user  = row[4]
                _entity.coupon = row[5]
                _entity.date_availability  = row[6]
                _entity.hour_availability  = row[7] 
                _entity.total_amount  = row[8]
                _entity.id_type_card  = row[9]
                _entity.document_number = row[10]
                _entity.expiration_year  = row[11]
                _entity.expiration_month  = row[12] 
                _entity.mail  = row[13]
                _entity.full_name_card  = row[14]
                _entity.status_sale = row[15]
                _entity.id_customer_address = row[20]
                _entity.address = row[21]
                
                _type_sales = []
                if _id_old  != _entity.id :
                    for se in _rows:
                        if row[0] == se[0]:
                            _typeSaleResponseEntity = typeSaleResponseEntity()
                            _typeSaleResponseEntity.id = se[16]
                            _typeSaleResponseEntity.amount = se[17]
                            _typeSaleResponseEntity.id_sub_service = se[18]
                            _typeSaleResponseEntity.full_name = se[19]
                            _typeSaleResponseEntity.id_sale = _entity.id
                            _type_sales.append(_typeSaleResponseEntity)

                    _entity.type_sales = _type_sales
                    _id_old = _entity.id 
                    _data.append(_entity)

            _cur.close()
        except(Exception) as e:
            self.add_log(str(e),type(self).__name__)
        finally:
            if _db is not None:
                _db.disconnect()
                print("Se cerro la conexion")
        return _data

    def get_sale_by_id_user(self,id_user):
        _db = None
        _status = 1
        _data = []
        try:
            _id_user = id_user
            _db = Database()
            _db.connect(self.host,self.port,self.user,self.password,self.database)
            print('Se conecto a la bd')
            _con_client = _db.get_client()
            _sql = """SELECT s.id, 
                        id_type_availability, 
                        ta.full_name  as full_name_id_type_availability,
                        s.id_customer, 
                        id_user, 
                        coupon, 
                        to_char(date_availability,'DD-MM-YYYY') as date_availability, 
                        hour_availability, 
                        total_amount,  
                        id_type_card, 
                        document_number, 
                        expiration_year, 
                        expiration_month, 
                        mail, 
                        full_name_card, 
                        status_sale, 
                        ts.id        AS id_type_sale, 
                        ts.amount 	as amount_type_sale,
                        ts.id_sub_service, 
                        ss.full_name AS full_name_sub_service,
                        s.id_customer_address ,
                        ca.address 
                    FROM   main.sale s 
                        INNER JOIN main.type_sale ts 
                                ON s.id = ts.id_sale 
                        INNER JOIN main.sub_service ss 
                                ON ss.id = ts.id_sub_service 
                        INNER JOIN main.type_availability ta
       			                ON ta.id  = s.id_type_availability
                        INNER JOIN main.customer_address ca 
       			                ON ca.id  = s.id_customer_address  
                    WHERE  s.id_user = %s 
                        AND s.status = %s; """
                                        
            _cur = _con_client.cursor()
            _cur.execute(_sql,(_id_user,_status))
            _rows = _cur.fetchall()
            _id_old = None
            for row in _rows:
                _entity = saleResponseEntity()
                _entity.id  = row[0]
                _entity.id_type_availability  = row[1] 
                _entity.full_name_type_availability  = row[2]
                _entity.id_customer  = row[3]
                _entity.id_user  = row[4]
                _entity.coupon = row[5]
                _entity.date_availability  = row[6]
                _entity.hour_availability  = row[7] 
                _entity.total_amount  = row[8]
                _entity.id_type_card  = row[9]
                _entity.document_number = row[10]
                _entity.expiration_year  = row[11]
                _entity.expiration_month  = row[12] 
                _entity.mail  = row[13]
                _entity.full_name_card  = row[14]
                _entity.status_sale = row[15]
                _entity.id_customer_address = row[20]
                _entity.address = row[21]
                
                _type_sales = []
                if _id_old  != _entity.id :
                    for se in _rows:
                        if row[0] == se[0]:
                            _typeSaleResponseEntity = typeSaleResponseEntity()
                            _typeSaleResponseEntity.id = se[16]
                            _typeSaleResponseEntity.amount = se[17]
                            _typeSaleResponseEntity.id_sub_service = se[18]
                            _typeSaleResponseEntity.full_name = se[19]
                            _typeSaleResponseEntity.id_sale = _entity.id
                            _type_sales.append(_typeSaleResponseEntity)

                    _entity.type_sales = _type_sales
                    _id_old = _entity.id 
                    _data.append(_entity)

            _cur.close()
        except(Exception) as e:
            self.add_log(str(e),type(self).__name__)
        finally:
            if _db is not None:
                _db.disconnect()
                print("Se cerro la conexion")
        return _data


