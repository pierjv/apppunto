from flask import Flask
from flask import Flask, jsonify, request
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_claims
)
from src.models.userModel import userModel
from src.entities.userEntity import userEntity
from src.controllers.userController import userController
from src.cn.data_base_connection import Database
from src.controllers.userStoreController import userStoreController
from src.controllers.serviceController import serviceController
from src.controllers.loginController import loginController
from src.controllers.userDateAvailabilityController import userDateAvailabilityController
from flask import Flask, jsonify, request


app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'simirasestotupcexplota' 
jwt = JWTManager(app)


@app.route('/token', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if username != 'test' or password != 'test':
        return jsonify({"message": "usuario o password errado"}), 401  
    ret = {'access_token': create_access_token(username)}
    return jsonify(ret), 200

@app.route('/login', methods=['POST'])
@jwt_required
def login_user(index):
    return loginController().login_user(request)

@app.route('/recover/<int:index>', methods=['GET'])
#@jwt_required
def recover_password(index):
    return loginController().recover_password(index)


@app.route('/load', methods=['GET'])
#@jwt_required
def load():
    return serviceController().get_services_load()

@app.route('/services', methods=['GET'])
#@jwt_required
def get_services():
    return serviceController().get_services()

@app.route('/services/<int:index>', methods=['GET'])
#@jwt_required
def get_services_by_user(index):
    return serviceController().get_services_by_user(index)

@app.route('/userdateavailability/<int:index>', methods=['GET'])
#@jwt_required
def get_user_date_availability_by_user(index):
    return userDateAvailabilityController().get_user_date_availability_by_user(index)

@app.route('/userdateavailability', methods=['POST'])
#@jwt_required
def update_user_date_availability():
    return userDateAvailabilityController().update_user_date_availability(request)

@app.route('/users', methods=['GET'])
@jwt_required
def get_users():
    return userController().get_users()

@app.route('/users', methods=['POST'])
#@jwt_required
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

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)

