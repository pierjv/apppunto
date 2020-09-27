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
    
    def charge_culqi(self,cvv,card_number,expiration_year,expiration_month,email,amount,description):
        try:
            public_key = self.culqi_public_key
            private_key = self.culqi_private_key
            client = pp(public_key=public_key, private_key=private_key)
            _amount = int(amount * 100)
            print('Inicio pasarela de pago CARD')
            
            token_data = {
                "cvv": cvv,
                "card_number": card_number,
                "expiration_year": expiration_year,
                "expiration_month": expiration_month,
                "email": email,
            }
            print('Inicio pasarela de pago TOKEN')
            token = client.token.create(data=token_data)

            if token["data"]["object"] == "error":
                charge = token
            else:
                charge_data = {
                    "amount": _amount,
                    "currency_code":"PEN",
                    "description": description,
                    "email": email,
                    "source_id": token["data"]["id"],
                }
                charge = client.charge.create(data = charge_data)
                print('Finalizo pasarela de pago')

            print(charge["data"]["object"])
            return charge["data"]
            
        except(Exception) as e:
            self.add_log(str(e),type(self).__name__)

    def add_card_culqi(self,cvv,card_number,expiration_year,expiration_month,email):
        try:
            public_key = self.culqi_public_key
            private_key = self.culqi_private_key
            client = pp(public_key=public_key, private_key=private_key)
            print('Inicio de verificar tarjeta en  pasarela de pago')
            
            token_data = {
                "cvv": cvv,
                "card_number": card_number,
                "expiration_year": expiration_year,
                "expiration_month": expiration_month,
                "email": email,
            }
            token = client.token.create(data=token_data)
            print('Fin de verificar tarjeta en  pasarela de pago')
            return token["data"]
            
        except(Exception) as e:
            self.add_log(str(e),type(self).__name__)

