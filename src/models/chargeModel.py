import culqi
try:
    from culqi.client import Client  as pp
except(Exception) as e:
    from culqi.client import Culqi  as pp
from src.models.dbModel import dbModel

class chargeModel(dbModel):

    def __init__(self):
        dbModel.__init__(self)
    
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
