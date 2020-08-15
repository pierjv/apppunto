from flask import Flask, jsonify, request
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_claims
)
import timedelta
from src.models.userModel import userModel
from src.entities.userEntity import userEntity
from src.controllers.userController import userController
from src.cn.data_base_connection import Database
from src.controllers.userStoreController import userStoreController
from src.controllers.serviceController import serviceController
from src.controllers.loginController import loginController
from src.controllers.userDateAvailabilityController import userDateAvailabilityController
from src.entities.loginEntity import tokenEntity
from src.controllers.customerController import customerController
from src.controllers.notificationController import notificationController
from src.controllers.chargeController import chargeController

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'cambiar_no_olvidar' 
jwt = JWTManager(app)

@jwt.expired_token_loader
def my_expired_token_callback(expired_token):
    token_type = expired_token['type']
    return jsonify({
        'status': 401,
        'sub_status': 42,
        'msg': 'El {} token ha expirado'.format(token_type)
    }), 401



@app.route('/token', methods=['POST'])
def get_token():
    _entity = tokenEntity()
    if _entity.validate_request(request):
        _expires = timedelta.Timedelta(weeks=1)
        _token = create_access_token(_entity.user, expires_delta=_expires)
        _ret = {'access_token': _token}
        return jsonify(_ret), 200
    return jsonify({"message": "usuario o password errado"}), 401  

@app.route('/login', methods=['POST'])
@jwt_required
def login_user():
    return loginController().login_user(request)

@app.route('/logincustomer', methods=['POST'])
#@jwt_required
def login_customer():
    return loginController().login_customer(request)

@app.route('/recover/<int:index>', methods=['GET'])
@jwt_required
def recover_password(index):
    return loginController().recover_password(index)

@app.route('/load', methods=['GET'])
def load():
    return loginController().get_load()

@app.route('/services', methods=['GET'])
@jwt_required
def get_services():
    return serviceController().get_services()

@app.route('/services/<int:index>', methods=['GET'])
@jwt_required
def get_services_by_user(index):
    return serviceController().get_services_by_user(index)

@app.route('/userservice/<int:index>', methods=['GET'])
@jwt_required
def get_user_by_id_service(index):
    return userController().get_user_by_id_service(index)

@app.route('/customer', methods=['POST'])
@jwt_required
def add_customer():
    return customerController().add_customer(request)

@app.route('/subservice/<int:index>', methods=['GET'])
@jwt_required
def get_sub_services_by_id_user(index):
    return serviceController().get_sub_services_by_id_user(index)

@app.route('/rate', methods=['POST'])
@jwt_required
def add_customer_rate():
    return customerController().add_customer_rate(request)

@app.route('/userdateavailability/<int:index>', methods=['GET'])
@jwt_required
def get_user_date_availability_by_user(index):
    return userDateAvailabilityController().get_user_date_availability_by_user(index)

@app.route('/userdateavailability', methods=['POST'])
@jwt_required
def update_user_date_availability():
    return userDateAvailabilityController().update_user_date_availability(request)

@app.route('/users', methods=['GET'])
@jwt_required
def get_users():
    return userController().get_users()

@app.route('/users', methods=['POST'])
@jwt_required
def add_user():
    return userController().add_user(request)

@app.route('/users/<int:index>', methods=['PUT'])
@jwt_required
def update_user(index):
    return userController().update_user(request,index)

@app.route('/users/<int:index>', methods=['DELETE'])
@jwt_required
def delete_user(index):
    return userController().delete_user(index)

@app.route('/userstores/<int:index>', methods=['GET'])
@jwt_required
def get_user_stores(index):
    return userStoreController().get_user_stores(index)

@app.route('/send', methods=['GET'])
#@jwt_required    #pushController().send_message()
def send_message():
    return notificationController().send_push_message()

@app.route('/charge', methods=['GET'])
#@jwt_required    #pushController().send_message()
def charge():
    #print(timedelta)
    #print(culqi)
    #print(culqi.client)
    #print (dir(culqi))
    #print (dir(culqi.client))

    #client = cul.Culqi(public_key=public_key, private_key=private_key)
    #print(culqi.client.Culqi)
    return chargeController().charge()


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)

