from flask import Flask, jsonify, request, render_template,redirect
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
from src.controllers.saleController import saleController
import os
from src.controllers.uploadController import uploadController
import hashlib
from src.controllers.codeController import codeController

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'cambiar_no_olvidar' 
#app.config["IMAGE_UPLOADS"] = "./static/"
app.config["IMAGE_UPLOADS"] = "/tmp"
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
@jwt_required
def login_customer():
    return loginController().login_customer(request)

@app.route('/recoveruser', methods=['POST'])
@jwt_required
def recover_password_user():
    return loginController().recover_password_user(request)

@app.route('/recovercustomer', methods=['POST'])
@jwt_required
def recover_password_customer():
    return loginController().recover_password_customer(request)

@app.route('/load/<int:index>', methods=['GET'])
def load(index):
    return loginController().get_load(index)

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

@app.route('/userdetail/<int:index>', methods=['GET'])
@jwt_required
def get_user_detail(index):
    return userController().get_user_detail(index)

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
    return chargeController().charge()

@app.route('/sale', methods=['POST'])
#@jwt_required
def add_sale():
    return saleController().add_sale(request)

@app.route('/sha', methods=['GET'])
#@jwt_required
def sha():
    cipher = codeController('92923923923123412341234188888234')
    encrypted = cipher.encrypt('hola')
    #decrypted = cipher.decrypt(encrypted)
    #print(encrypted)
    #print(decrypted)
    return 'OK'

################################### WEB ADMIN ###################################################
#################################################################################################

@app.route('/webadmin', methods=['GET'])
def web_admin():
    return render_template('index.html')

@app.route('/wa_services', methods=['GET'])
def wa_services():
    print('1')
    return render_template('wa_services.html')

@app.route('/wa_sub_services', methods=['GET'])
def wa_sub_services():
    print('1')
    return render_template('wa_sub_services.html')

@app.route('/wa_dashboard', methods=['GET'])
def wa_dashboard():
    print('1')
    return render_template('wa_dashboard.html')

# Route to upload image
@app.route("/upload-image", methods=["GET", "POST"])
def upload_image():
    if request.method == "POST":
        if request.files:
            image = request.files["image"]
            print('1')
            print(image)    
            print(os.path.join(app.config["IMAGE_UPLOADS"]))
            print(image.filename)
            print(os.path.join(app.config["IMAGE_UPLOADS"], image.filename))
            path_image = os.path.join(app.config["IMAGE_UPLOADS"], image.filename)
            image.save(os.path.join(app.config["IMAGE_UPLOADS"], image.filename))   
            print('2')               
            with open(path_image,"rb") as f:
                z=f.read()
                print(z)
                serviceController().update_file_image(z)                        
            return redirect(request.url)
    return render_template("upload_image.html")
    
    #uploadController().get()
    #uploadController().implicit()

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)

