from flask import Flask, jsonify, request
from src.cn.data_base_connection import Database
from src.models.dbModel import dbModel
from src.entities.userEntity import userEntity,userDetailEntity,rateEntity,commentEntity, dashboardEntity ,dashboardServiceEntity
from src.entities.serviceEntity import serviceEntity
from src.entities.subServiceEntity import subServiceEntity
from src.entities.userStoreEntity import userStoreEntity


class userModel(dbModel):

    def __init__(self):
        dbModel.__init__(self)

    def add_user(self,userEntity):
        _db = None
        _id_user = 0
        _status = 1
        _i = 0
        try:
            _db = Database()
            _db.connect(self.host,self.port,self.user,self.password,self.database)
            print('Se conecto a la bd')
            _con_client = _db.get_client()
            _sql = """INSERT INTO main.user_p (mail,social_name,full_name,document_number,type_user,photo,
                      cellphone,about,password,id_type_document,status) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id;"""
            _cur = _con_client.cursor()
            _cur.execute(_sql, (userEntity.mail,userEntity.social_name,userEntity.full_name,
                                userEntity.document_number,userEntity.type_user,
                                userEntity.photo,userEntity.cellphone,userEntity.about,userEntity.password,
                                userEntity.id_type_document,_status))
            _id_user = _cur.fetchone()[0]
            userEntity.id = _id_user
            
            _sql_store = """INSERT INTO main.user_store (id_user, full_name, address, longitude, latitude, main, status) 
                            VALUES(%s,%s,%s,%s,%s,%s,%s) RETURNING id;"""
            for us in userEntity.user_store:
                _cur.execute(_sql_store, (_id_user,us.full_name,us.address,us.longitude,us.latitude,us.main,_status))
                _id_user_store = _cur.fetchone()[0]
                userEntity.user_store[_i].id = _id_user_store
                userEntity.user_store[_i].id_user = _id_user
                _i += 1

            _con_client.commit()
            _cur.close()
        except(Exception) as e:
            self.add_log(str(e),type(self).__name__)
        finally:
            if _db is not None:
                _db.disconnect()
                print("Se cerro la conexion")
        return userEntity

    def delete_user(self,id):
        _db = None
        _status = 0
        _id = id
        try:
            _db = Database()
            _db.connect(self.host,self.port,self.user,self.password,self.database)
            print('Se conecto a la bd')
            _con_client = _db.get_client()
            _sql = """UPDATE main.user_p SET status = %s WHERE id = %s;"""
            _cur = _con_client.cursor()
            _cur.execute(_sql, (_status,_id))
            _con_client.commit()
            _cur.close()
        except(Exception) as e:
            self.add_log(str(e),type(self).__name__)
        finally:
            if _db is not None:
                _db.disconnect()
                print("Se cerro la conexion")
        return _id
    
    def get_users(self):
        _db = None
        _status = 0
        _id = id
        _data_row = []
        try:
            _db = Database()
            _db.connect(self.host,self.port,self.user,self.password,self.database)
            print('Se conecto a la bd')
            _con_client = _db.get_client()
            _sql = """SELECT u.id, 
                u.mail, 
                u.social_name, 
                u.full_name, 
                u.id_type_document, 
                u.document_number, 
                u.type_user, 
                u.photo, 
                u.cellphone, 
                u.about, 
                us.id        AS id_user_store, 
                us.full_name AS name_user_store, 
                us.address, 
                us.longitude, 
                us.latitude, 
                us.main, 
                a.avg_rate
            FROM   main.user_p u 
                INNER JOIN main.user_store us 
                        ON u.id = us.id_user
                left JOIN (SELECT id_user, 
                                    Avg(rate) :: float4 AS avg_rate 
                            FROM   main.customer_rate 
                            GROUP  BY 1) a 
                        ON a.id_user = u.id  
            WHERE  u.status = 1 
                AND us.status = 1 
            ORDER  BY 1; """
            _cur = _con_client.cursor()
            _cur.execute(_sql)
            _rows = _cur.fetchall()
            
            _id_user_old = None
            for row in _rows:
                _userEntity= userEntity()
                _userEntity.id  = row[0]
                _userEntity.mail  = row[1] 
                _userEntity.social_name  = row[2]
                _userEntity.full_name  = row[3]
                _userEntity.id_type_document  = row[4]
                _userEntity.document_number  = row[5]
                _userEntity.type_user  = row[6]
                _userEntity.photo  = row[7]
                _userEntity.cellphone  = row[8]
                _userEntity.about  = row[9]
                _avg_rate =  row[16]
                if _avg_rate is None:
                    _avg_rate = 0
                _userEntity.avg_rate = _avg_rate
                _user_stores = []
                if _id_user_old  != _userEntity.id :
                    for se in _rows:
                        if row[0] == se[0] and _userEntity is not None:
                            _userStoreEntity = userStoreEntity()
                            _userStoreEntity.id = se[10]
                            _userStoreEntity.full_name = se[11]
                            _userStoreEntity.address = se[12]
                            _userStoreEntity.longitude = se[13]
                            _userStoreEntity.latitude = se[14]
                            _userStoreEntity.main = se[15]
                            _userStoreEntity.id_user = _userEntity.id 
                            _user_stores.append(_userStoreEntity)

                    _userEntity.user_store = _user_stores
                    _data_row.append(_userEntity)
                    _id_user_old = _userEntity.id 

            _cur.close()
        except(Exception) as e:
            self.add_log(str(e),type(self).__name__)
        finally:
            if _db is not None:
                _db.disconnect()
                print("Se cerro la conexion")
        return _data_row

    def get_user_by_id(self,id):
        _db = None
        _status = 1
        _entity = None
        _id_user = id
        try:
            _db = Database()
            _db.connect(self.host,self.port,self.user,self.password,self.database)
            print('Se conecto a la bd')
            _con_client = _db.get_client()

            _sql = """SELECT up.id, 
                        up.mail, 
                        up.social_name, 
                        up.full_name, 
                        up.id_type_document, 
                        up.document_number, 
                        up.type_user, 
                        up.photo, 
                        up.cellphone,
                        up.about
                    FROM   main.user_p up 
                    WHERE  up.status = %s
                        AND id = %s; """   

            _cur = _con_client.cursor()
            _cur.execute(_sql,(_status,_id_user,))
            _rows = _cur.fetchall()
        
            if len(_rows) >= 1:
                _entity= userEntity()
                _entity.id  = _rows[0][0]
                _entity.mail  = _rows[0][1] 
                _entity.social_name  = _rows[0][2]
                _entity.full_name  = _rows[0][3]
                _entity.id_type_document  = _rows[0][4]
                _entity.document_number  = _rows[0][5]
                _entity.type_user  = _rows[0][6]
                _entity.photo  = _rows[0][7]
                _entity.cellphone  = _rows[0][8]
                _entity.about  = _rows[0][9]

            _cur.close()
        except(Exception) as e:
            self.add_log(str(e),type(self).__name__)
        finally:
            if _db is not None:
                _db.disconnect()
                print("Se cerro la conexion")
        return _entity

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

            _sql = """SELECT up."password", up.cellphone
                    FROM   main.user_p up 
                    WHERE  up.status = %s
                        AND mail = %s; """   

            _cur = _con_client.cursor()
            _cur.execute(_sql,(_status,_mail,))
            _rows = _cur.fetchall()
        
            if len(_rows) >= 1:
                _entity  = userEntity()
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

    def get_user_by_id_service(self,idService):
        _db = None
        _status = 1
        _id_service = idService
        _data_row =[]
        try:
            _db = Database()
            _db.connect(self.host,self.port,self.user,self.password,self.database)
            print('Se conecto a la bd')
            _con_client = _db.get_client()

            _sql = """SELECT u.id, 
                    u.mail, 
                    u.social_name, 
                    u.full_name, 
                    u.id_type_document, 
                    u.document_number, 
                    u.type_user, 
                    u.photo, 
                    u.cellphone, 
                    u.about, 
                    us.id        AS id_user_store, 
                    us.full_name AS name_user_store, 
                    us.address, 
                    us.longitude, 
                    us.latitude, 
                    us.main, 
                    a.avg_rate 
                FROM   main.user_p u 
                    inner join main.user_store us 
                            ON u.id = us.id_user 
                    inner join main.user_service USE 
                            ON u.id = USE.id_user 
                    left join (SELECT id_user, 
                                        Avg(rate) :: float4 AS avg_rate 
                                FROM   main.customer_rate 
                                GROUP  BY 1) a 
                            ON a.id_user =  u.id 
                    WHERE  u.status = %s and us.status = %s
                        AND use.id_service = %s;"""   

            _cur = _con_client.cursor()
            _cur.execute(_sql,(_status,_status,_id_service,))
            _rows = _cur.fetchall()

            _id_user_old = None
            for row in _rows:
                _userEntity= userEntity()
                _userEntity.id  = row[0]
                _userEntity.mail  = row[1] 
                _userEntity.social_name  = row[2]
                _userEntity.full_name  = row[3]
                _userEntity.id_type_document  = row[4]
                _userEntity.document_number  = row[5]
                _userEntity.type_user  = row[6]
                _userEntity.photo  = row[7]
                _userEntity.cellphone  = row[8]
                _userEntity.about  = row[9]
                _avg_rate =  row[16]
                if _avg_rate is None:
                    _avg_rate = 0
                _userEntity.avg_rate = _avg_rate
                _user_stores = []
                if _id_user_old  != _userEntity.id :
                    for se in _rows:
                        if row[0] == se[0] and _userEntity is not None:
                            _userStoreEntity = userStoreEntity()
                            _userStoreEntity.id = se[10]
                            _userStoreEntity.full_name = se[11]
                            _userStoreEntity.address = se[12]
                            _userStoreEntity.longitude = se[13]
                            _userStoreEntity.latitude = se[14]
                            _userStoreEntity.main = se[15]
                            _userStoreEntity.id_user = _userEntity.id 
                            _user_stores.append(_userStoreEntity)

                    _userEntity.user_store = _user_stores
                    _data_row.append(_userEntity)
                    _id_user_old = _userEntity.id 

            _cur.close()
        except(Exception) as e:
            self.add_log(str(e),type(self).__name__)
        finally:
            if _db is not None:
                _db.disconnect()
                print("Se cerro la conexion")
        return _data_row

    def update_user(self,userEntity):
        _db = None
        _id_user = 0
        _status = 1
        try:
            _db = Database()
            _db.connect(self.host,self.port,self.user,self.password,self.database)
            print('Se conecto a la bd')
            _con_client = _db.get_client()
            _sql = """UPDATE main.user_p SET  mail= %s, social_name= %s, full_name= %s, id_type_document= %s, document_number= %s, 
                      type_user= %s, photo= %s cellphone=%s, about=%s WHERE id = %s and status = %s;"""
            _cur = _con_client.cursor()
            _cur.execute(_sql, (userEntity.mail,userEntity.social_name,userEntity.full_name,
                                userEntity.id_type_document,userEntity.document_number,userEntity.type_user,
                                userEntity.photo,userEntity.cellphone,userEntity.about,userEntity.id,_status))
            _id_user = userEntity.id
            _con_client.commit()
            _cur.close()
        except(Exception) as e:
            self.add_log(str(e),type(self).__name__)
        finally:
            if _db is not None:
                _db.disconnect()
                print("Se cerro la conexion")
        return _id_user

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
                    FROM   main.user_p p 
                    WHERE p.mail = %s;"""   
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

    def get_user_detail(self,id):
        _db = None
        _status = 1
        _data_services = []
        _data_rates = []
        _data_comments = []
        _id_user = id
        _userDetailEntity= None
        try:
            _userDetailEntity = userDetailEntity()
            _db = Database()
            _db.connect(self.host,self.port,self.user,self.password,self.database)
            print('Se conecto a la bd')
            _con_client = _db.get_client()
            
            _sql = """SELECT uss.id_service, 
                    s.full_name  AS service_name, 
                    us."enable"  AS service_enable, 
                    uss.id_sub_service, 
                    ss.full_name AS sub_service_name, 
                    uss.charge, 
                    uss."enable" AS sub_service_enable,
                    ss.in_filter 
                FROM   main.user_sub_service uss 
                    INNER JOIN main.sub_service ss 
                            ON ss.id = uss.id_sub_service 
                    INNER JOIN main.service s 
                            ON uss.id_service = s.id 
                    INNER JOIN main.user_p up 
                            ON uss.id_user = up.id 
                    INNER JOIN main.user_service us 
                            ON us.id_service = uss.id_service 
                            AND us.id_user  = uss.id_user
                WHERE  up.status = %s
                    AND uss."enable" = 1 
                    AND us."enable" = 1 
                    AND uss.id_user = %s 
                ORDER  BY 1; """
                                        
            _cur = _con_client.cursor()
            _cur.execute(_sql,(_status,_id_user,))
            _rows = _cur.fetchall()
            _id_service_old = None
            for row in _rows:
                _serviceEntity = serviceEntity()
                _serviceEntity.id  = row[0]
                _serviceEntity.full_name  = row[1] 
                _serviceEntity.enable  = row[2]
                _sub_services = []              
                if _id_service_old  != _serviceEntity.id :
                    for se in _rows:
                        if row[0] == se[0]:
                            _subServiceEntity = subServiceEntity()
                            _subServiceEntity.id = se[3]
                            _subServiceEntity.full_name = se[4]
                            _subServiceEntity.charge = se[5]
                            _subServiceEntity.enable = se[6]
                            _subServiceEntity.id_service = se[0]
                            _subServiceEntity.in_filter = se[7]
                            _subServiceEntity.id_service = _serviceEntity.id 
                            _sub_services.append(_subServiceEntity)

                    _serviceEntity.sub_services = _sub_services
                    _data_services.append(_serviceEntity)
                    _id_service_old = _serviceEntity.id 

            _userDetailEntity.services = _data_services

            _sql_rate = """SELECT cr.rate, 
                        a.qua 						    AS total, 
                        Count(cr.id_user)               AS quantity, 
                        (Count(cr.id_user) * 1.0 / a.qua)::float4 AS percentage 
                    FROM   main.customer_rate cr 
                        INNER JOIN (SELECT id_user, 
                                            Count(id_user) AS qua 
                                    FROM   main.customer_rate 
                                    WHERE  id_user = %s
                                    GROUP  BY 1) a 
                                ON a.id_user = cr.id_user 
                    GROUP  BY 1, 2; """

            _cur.execute(_sql_rate,(_id_user,))
            _rows = _cur.fetchall()
            for row in _rows:
                _rateEntity = rateEntity()
                _rateEntity.rate = row[0]
                _rateEntity.total = row[1]
                _rateEntity.quantity = row[2]
                _rateEntity.percentage = row[3]
                _data_rates.append(_rateEntity)
            
            _userDetailEntity.rates = _data_rates

            _sql_comment = """ SELECT cr.rate, 
                    cr.description, 
                    To_char(cr.date_transaction, 'DD-MM-YYYY') AS date_transaction, 
                    c.full_name 
                FROM   main.customer_rate cr 
                    INNER JOIN main.customer c 
                            ON cr.id_customer = c.id 
                WHERE  id_user = %s
                ORDER BY cr.date_transaction desc
                LIMIT 10; """

            _cur.execute(_sql_comment,(_id_user,))
            _rows = _cur.fetchall()
            for row in _rows:
                _commentEntity = commentEntity()
                _commentEntity.rate = row[0]
                _commentEntity.description = row[1]
                _commentEntity.date_transaction = row[2]
                _commentEntity.full_name = row[3]
                _data_comments.append(_commentEntity)
            
            _userDetailEntity.comments = _data_comments

            _cur.close()
        except(Exception) as e:
            self.add_log(str(e),type(self).__name__)
        finally:
            if _db is not None:
                _db.disconnect()
                print("Se cerro la conexion")
        return _userDetailEntity
    
    def get_dashboard_general(self):
        _db = None
        _entity = None
        try:
            _db = Database()
            _db.connect(self.host,self.port,self.user,self.password,self.database)
            print('Se conecto a la bd')
            _con_client = _db.get_client()

            _sql = """SELECT (SELECT Count(*) AS users 
                        FROM   main.user_p up 
                        WHERE  up.status = 1) AS users, 
                    (SELECT Count(*) AS customers 
                        FROM   main.customer c 
                        WHERE  c.status = 1)  AS customers, 
                    s.total_amount, 
                    s.sales, 
                    s.average_amount :: FLOAT4, 
                    h.max_hour_availability, 
                    a.sales_per_day, 
                    a.amount_per_day 
                FROM   (SELECT Sum(s.total_amount) AS total_amount, 
                            Count(s.id)         AS sales, 
                            Avg(s.total_amount) AS average_amount 
                        FROM   main.sale s 
                        WHERE  s.status = 1) s, 
                    (SELECT s.hour_availability AS max_hour_availability, 
                            Count(s.id)         AS sales 
                        FROM   main.sale s 
                        WHERE  s.status  = 1
                        GROUP  BY 1 
                        ORDER  BY 2 DESC 
                        LIMIT  1) h, 
                    (SELECT Avg(a.sales)                  AS sales_per_day, 
                            Avg(a.total_amount) :: FLOAT4 AS amount_per_day 
                        FROM   (SELECT s.date_availability, 
                                    Count(s.id)         AS sales, 
                                    Sum(s.total_amount) AS total_amount 
                                FROM   main.sale s 
                                WHERE  s.status = 1 
                                GROUP  BY 1) AS a) AS a;"""   

            _cur = _con_client.cursor()
            _cur.execute(_sql)
            _rows = _cur.fetchall()
        
            if len(_rows) >= 1:
                _entity= dashboardEntity()
                _entity.users  = _rows[0][0]
                _entity.customers  = _rows[0][1] 
                _entity.total_amount  = _rows[0][2]
                _entity.sales  = _rows[0][3]
                _entity.average_amount  = _rows[0][4]
                _entity.max_hour_availability  = _rows[0][5]
                _entity.sales_per_day  = _rows[0][6]
                _entity.amount_per_day  = _rows[0][7]

            _cur.close()
        except(Exception) as e:
            self.add_log(str(e),type(self).__name__)
        finally:
            if _db is not None:
                _db.disconnect()
                print("Se cerro la conexion")
        return _entity
    
    def get_dashboard_service(self):
        _db = None
        _entity = None
        _data_dashboard_services = []
        try:
            _db = Database()
            _db.connect(self.host,self.port,self.user,self.password,self.database)
            print('Se conecto a la bd')
            _con_client = _db.get_client()

            _sql = """DELETE FROM main.service_dashboard; 

                    INSERT INTO main.service_dashboard 
                                (id_service, 
                                service) 
                    SELECT id, 
                        full_name 
                    FROM   main.service s 
                    ORDER  BY 1; 

                    UPDATE main.service_dashboard a 
                    SET    users = b.users, 
                        sales = b.sales, 
                        amount = b.amount, 
                        average_sale = b.average_sale 
                    FROM   (SELECT ss.id_service, 
                                Count(ts.id)              AS sales, 
                                Sum(ts.amount)            AS amount, 
                                Count(DISTINCT s.id_user) AS users, 
                                Avg(ts.amount)            AS average_sale 
                            FROM   main.type_sale ts 
                                INNER JOIN main.sub_service ss 
                                        ON ts.id_sub_service = ss.id 
                                INNER JOIN main.sale s 
                                        ON ts.id_sale = s.id 
                            GROUP  BY 1) b 
                    WHERE  a.id_service = b.id_service; 


                    UPDATE main.service_dashboard a 
                    SET    max_hour_availability = d.hour_availability 
                    FROM   (SELECT b.hour_availability, 
                                b.id_service, 
                                b.quantity 
                            FROM   (SELECT s.hour_availability, 
                                        ss.id_service, 
                                        Count(s.id) AS quantity 
                                    FROM   main.sale s 
                                        INNER JOIN main.type_sale ts 
                                                ON s.id = ts.id_sale 
                                        INNER JOIN main.sub_service ss 
                                                ON ss.id = ts.id_sub_service 
                                    WHERE  s.status = 1 
                                    GROUP  BY 1, 
                                            2) b 
                                INNER JOIN (SELECT a.id_service, 
                                                    Max(a.quantity) AS quantity 
                                            FROM   (SELECT s.hour_availability, 
                                                            ss.id_service, 
                                                            Count(s.id) AS quantity 
                                                    FROM   main.sale s 
                                                            INNER JOIN main.type_sale ts 
                                                                    ON s.id = ts.id_sale 
                                                            INNER JOIN main.sub_service ss 
                                                                    ON ss.id = ts.id_sub_service 
                                                    WHERE  s.status = 1 
                                                    GROUP  BY 1, 
                                                                2) a 
                                            GROUP  BY 1) c 
                                        ON b.id_service = c.id_service 
                                            AND b.quantity = c.quantity) d 
                    WHERE  a.id_service = d.id_service; 
                   
                    DELETE FROM main.service_dashboard_aux; 

                    INSERT INTO main.service_dashboard_aux 
                                (number_day, 
                                id_service, 
                                average_sales, 
                                average_amount) 
                    SELECT Extract(dow FROM date_availability)                AS number_day, 
                        ss.id_service, 
                        Count(ts.id) / Count(DISTINCT s.date_availability) AS average_sales, 
                        Avg(ts.amount)                                     AS average_amount 
                    FROM   main.sale s 
                        INNER JOIN main.type_sale ts 
                                ON s.id = ts.id_sale 
                        INNER JOIN main.sub_service ss 
                                ON ss.id = ts.id_sub_service 
                    GROUP  BY 1, 
                            2; 

                    UPDATE main.service_dashboard a 
                    SET    sales_q_1 = b.average_sales, 
                        sales_a_1 = b.average_amount 
                    FROM   main.service_dashboard_aux b 
                    WHERE  a.id_service = b.id_service 
                        AND b.number_day = 1; 

                    UPDATE main.service_dashboard a 
                    SET    sales_q_2 = b.average_sales, 
                        sales_a_2 = b.average_amount 
                    FROM   main.service_dashboard_aux b 
                    WHERE  a.id_service = b.id_service 
                        AND b.number_day = 2; 

                    UPDATE main.service_dashboard a 
                    SET    sales_q_3 = b.average_sales, 
                        sales_a_3 = b.average_amount 
                    FROM   main.service_dashboard_aux b 
                    WHERE  a.id_service = b.id_service 
                        AND b.number_day = 3; 

                    UPDATE main.service_dashboard a 
                    SET    sales_q_4 = b.average_sales, 
                        sales_a_4 = b.average_amount 
                    FROM   main.service_dashboard_aux b 
                    WHERE  a.id_service = b.id_service 
                        AND b.number_day = 4; 

                    UPDATE main.service_dashboard a 
                    SET    sales_q_5 = b.average_sales, 
                        sales_a_5 = b.average_amount 
                    FROM   main.service_dashboard_aux b 
                    WHERE  a.id_service = b.id_service 
                        AND b.number_day = 5; 

                    UPDATE main.service_dashboard a 
                    SET    sales_q_6 = b.average_sales, 
                        sales_a_6 = b.average_amount 
                    FROM   main.service_dashboard_aux b 
                    WHERE  a.id_service = b.id_service 
                        AND b.number_day = 6; 

                    UPDATE main.service_dashboard a 
                    SET    sales_q_7 = b.average_sales, 
                        sales_a_7 = b.average_amount 
                    FROM   main.service_dashboard_aux b 
                    WHERE  a.id_service = b.id_service 
                        AND b.number_day = 0; 

                    commit;
                    select * from main.service_dashboard sd order by 1;"""   

            _cur = _con_client.cursor()
            _cur.execute(_sql)
            _rows = _cur.fetchall()

            for row in _rows:
                _entity= dashboardServiceEntity()
                _entity.id_service  = row[0]
                _entity.service  = row[1] 
                _entity.users  = row[2]
                _entity.amount  = row[3]
                _entity.sales  = row[4]
                _entity.average_sale  = row[5]
                _entity.max_hour_availability  = row[6]
                _entity.sales_q_1  = row[7]
                _entity.sales_q_2  = row[8]
                _entity.sales_q_3  = row[9]
                _entity.sales_q_4  = row[10] 
                _entity.sales_q_5  = row[11]
                _entity.sales_q_6  = row[12]
                _entity.sales_q_7  = row[13]
                _entity.sales_a_1  = row[14]
                _entity.sales_a_2  = row[15]
                _entity.sales_a_3  = row[16]
                _entity.sales_a_4  = row[17]
                _entity.sales_a_5  = row[18]
                _entity.sales_a_6  = row[19]
                _entity.sales_a_7  = row[20]
                _entity.valuesToFormat()
                _entity.classToFormat()
                _data_dashboard_services.append(_entity)

            _cur.close()
        except(Exception) as e:
            self.add_log(str(e),type(self).__name__)
        finally:
            if _db is not None:
                _db.disconnect()
                print("Se cerro la conexion")
        return _data_dashboard_services