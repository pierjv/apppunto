
import requests
import json
from src.controllers.responseController import responseController
import culqi
try:
    from culqi.client import Client  as pp
except(Exception) as e:
    from culqi.client import Culqi  as pp

class chargeController(responseController):

    def charge3(self):
        post_data =  {
            "amount": "744600",
            "currency_code": "PEN",
            "email": "richard@piedpiper.com",
            "source_id":"tkn_test_njKpZTL2C1hnbvos"   
        }
        URI_POST = 'https://api.culqi.com/v2/charges'
        headers = {'Authorization': 'Bearer sk_test_D54Fy8BFCuTAZsF7'}

        post_response = requests.post(url=URI_POST, json=post_data,headers=headers)
        print(post_response)
        return 'OK'
    
    def charge(self):
        public_key = 'pk_test_qnFaGRJ7pNaggBVs'
        private_key = 'sk_test_D54Fy8BFCuTAZsF7'
        print('token2')
        client = pp(public_key=public_key, private_key=private_key)
        token_data = {
            "cvv": "123",
            "card_number": "4111111111111111",
            "expiration_year": "2025",
            "expiration_month": "09",
            "email": "richard@piedpiper.com",
        }
        print('token')
        token = client.token.create(data=token_data)
        charge_data = {
            "amount":1000,
            "currency_code":"PEN",
            "description":"venta prueba",
            "email":"richard@piedpipddder.com",
            "source_id": token["data"]["id"],
        }
        charge = client.charge.create(data = charge_data)
        print('fin')
        #print(charge["data"])
        return charge["data"]

    def charge_culqi(self):
        public_key = 'pk_test_qnFaGRJ7pNaggBVs'
        private_key = 'sk_test_D54Fy8BFCuTAZsF7'
        print('token2')
        client = pp(public_key=public_key, private_key=private_key)
        token_data = {
            "cvv": "123",
            "card_number": "4111111111111111",
            "expiration_year": "2025",
            "expiration_month": "09",
            "email": "richard@piedpiper.com",
        }
        print('token')
        token = client.token.create(data=token_data)
        charge_data = {
            "amount":1000,
            "currency_code":"PEN",
            "description":"venta prueba",
            "email":"richard@piedpipddder.com",
            "source_id": token["data"]["id"],
        }
        charge = client.charge.create(data = charge_data)
        print('fin')
        #print(charge["data"])
        return charge["data"]
    '''def charge2(self):
        _e= None
        _data = None
        try:

            #public= pk_test_qnFaGRJ7pNaggBVs
            #privada = sk_test_D54Fy8BFCuTAZsF7
            public_key = 'pk_test_qnFaGRJ7pNaggBVs'
            private_key = 'sk_test_D54Fy8BFCuTAZsF7'

            client = Culqi(public_key=public_key, private_key=private_key)
            token_data = {
                "cvv": "123",
                "card_number": "4111111111111111",
                "expiration_year": "2025",
                "expiration_month": "09",
                "email": "richard@piedpiper.com",
            }
            print('token')
            token = client.token.create(data=token_data)
            charge_data = {
                "amount":1000,
                "currency_code":"PEN",
                "description":"venta prueba",
                "email":"richard@piedpipddder.com",
                "source_id": token["data"]["id"],
            }
            charge= client.charge.create(data = charge_data)
            print('fin')
            _data= charge["data"]

        except(Exception) as e:
            print('OK E')
            _e = e
        finally: 
            print('error: '+ str(_e))
        return _data'''