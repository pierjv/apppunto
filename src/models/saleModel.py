
from flask import Flask, jsonify, request
from src.cn.data_base_connection import Database
from src.models.dbModel import dbModel
from src.entities.serviceEntity import serviceEntity
from src.entities.subServiceEntity import subServiceEntity
from src.entities.saleEntity import saleEntity

class saleModel(dbModel):

    def __init__(self):
        dbModel.__init__(self)

    def add_sale(self,saleEntity):

        _db = None
        _id_user = 0
        _status = 1
        _i = 0
        try:
            _db = Database()
            _db.connect(self.host,self.port,self.user,self.password,self.database)
            print('Se conecto a la bd')
            _con_client = _db.get_client()
            _sql = """INSERT INTO main.sale (id_type_availability, id_customer, id_user, coupon, date_availability, hour_availability, total_amount,
                      status, date_transaction,id_type_card, document_number,expiration_year,expiration_month,mail,full_name_card)
                      VALUES(%s,%s,%s,%s,to_date(%s,'DD-MM-YYY'),%s,%s,%s,current_timestamp,%s,%s,%s,%s,%s,%s) RETURNING id;"""
            _cur = _con_client.cursor()
            _cur.execute(_sql, (saleEntity.id_type_availability,saleEntity.id_customer,saleEntity.id_user,
                                saleEntity.coupon,saleEntity.date_availability,saleEntity.hour_availability,
                                saleEntity.total_amount,_status,saleEntity.id_type_card,
                                saleEntity.document_number,saleEntity.expiration_year,saleEntity.expiration_month,
                                saleEntity.mail,saleEntity.full_name_card))
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