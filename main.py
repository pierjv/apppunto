from flask import Flask, jsonify, request, render_template,redirect,session
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_claims
)
import timedelta
from src.models.userModel import userModel
from src.entities.userEntity import userEntity,dashboardEntity
from src.controllers.userController import userController
from src.cn.data_base_connection import Database
from src.controllers.userStoreController import userStoreController
from src.controllers.serviceController import serviceController
from src.controllers.loginController import loginController
from src.controllers.userDateAvailabilityController import userDateAvailabilityController
from src.entities.loginEntity import tokenEntity
from src.entities.serviceEntity import serviceEntity
from src.entities.subServiceEntity import subServiceEntity
from src.controllers.customerController import customerController
from src.controllers.notificationController import notificationController
from src.controllers.chargeController import chargeController
from src.controllers.saleController import saleController
import os
from src.controllers.uploadController import uploadController
import hashlib
from src.controllers.codeController import codeController
from src.controllers.cryptoController import AESCipher


app = Flask(__name__)
app.secret_key = "any random string"
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

@app.route('/subservices', methods=['POST'])
def get_sub_services_by_id_service_and_id_user():
    return serviceController().get_sub_services_by_id_service_and_id_user(request)

@app.route('/userservice/<int:index>', methods=['GET'])
#@jwt_required
def get_user_by_id_service(index):
    return userController().get_user_by_id_service(index)

@app.route('/userserviceadd', methods=['POST'])
@jwt_required
def update_user_service():
    return userController().update_user_service(request)

@app.route('/usersubservice', methods=['POST'])
#@jwt_required
def get_user_by_sub_services():
    return userController().get_user_by_sub_services(request)

@app.route('/usersubserviceadd', methods=['POST'])
@jwt_required
def update_user_sub_service():
    return userController().update_user_sub_service(request)


@app.route('/userbankaccount/<int:index>', methods=['GET'])
@jwt_required
def get_user_bank_account_by_id_user(index):
    return userController().get_user_bank_account_by_id_user(index)

@app.route('/userbankaccount', methods=['POST'])
@jwt_required
def add_user_bank_account():
    return userController().add_user_bank_account(request)

@app.route('/userbankaccount', methods=['PUT'])
@jwt_required
def update_user_bank_account():
    return userController().update_user_bank_account(request)

@app.route('/userbankaccount/<int:index>', methods=['DELETE'])
@jwt_required
def delete_user_bank_account(index):
    return userController().delete_user_bank_account(index)



@app.route('/customer', methods=['POST'])
@jwt_required
def add_customer():
    return customerController().add_customer(request)

@app.route('/customer', methods=['PUT'])
@jwt_required
def update_customer():
    return customerController().update_customer(request)

@app.route('/customeraddress/<int:index>', methods=['GET'])
@jwt_required
def get_customer_address_by_id_customer(index):
    return customerController().get_customer_address_by_id_customer(index)

@app.route('/customeraddress', methods=['POST'])
@jwt_required
def add_customer_address():
    return customerController().add_customer_address(request)

@app.route('/customeraddress', methods=['PUT'])
@jwt_required
def update_customer_address():
    return customerController().update_customer_address(request)

@app.route('/customeraddress/<int:index>', methods=['DELETE'])
@jwt_required
def delete_customer_address(index):
    return customerController().delete_customer_address(index)

@app.route('/customercard/<int:index>', methods=['GET'])
@jwt_required
def get_customer_card_by_id_customer(index):
    return customerController().get_customer_card_by_id_customer(index)

@app.route('/customercard', methods=['POST'])
@jwt_required
def add_customer_card():
    return customerController().add_customer_card(request)

@app.route('/customercard/<int:index>', methods=['DELETE'])
@jwt_required
def delete_customer_card(index):
    return customerController().delete_customer_card(index)

@app.route('/customerfavorite', methods=['POST'])
@jwt_required
def update_customer_user_favorite():
    return customerController().update_customer_user_favorite(request)

@app.route('/userdetail/<int:index>/<int:id_customer>', methods=['GET'])
def get_user_detail(index,id_customer):
    return userController().get_user_detail(index,id_customer)

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
#@jwt_required
def get_users():
    return userController().get_users()

@app.route('/userstype/<int:index>', methods=['GET'])
#@jwt_required
def get_users_by_type(index):
    return userController().get_users_by_type(index)

@app.route('/userstypefilter', methods=['POST'])
#@jwt_required
def get_users_by_type_sub_services():
    return userController().get_users_by_type_sub_services(request)

@app.route('/users', methods=['POST'])
@jwt_required
def add_user():
    return userController().add_user(request)

@app.route('/users', methods=['PUT'])
@jwt_required
def update_user():
    return userController().update_user(request)

@app.route('/users/<int:index>', methods=['DELETE'])
@jwt_required
def delete_user(index):
    return userController().delete_user(index)

@app.route('/userstore/<int:index>', methods=['GET'])
@jwt_required
def get_user_stores_by_id_user(index):
    return userStoreController().get_user_stores_by_id_user(index)

@app.route('/userstore', methods=['POST'])
@jwt_required
def add_user_store():
    return userStoreController().add_user_store(request)

@app.route('/userstore/<int:index>', methods=['DELETE'])
@jwt_required
def delete_user_store(index):
    return userStoreController().delete_user_store(index)


@app.route('/send', methods=['GET'])
#@jwt_required    #pushController().send_message()
def send_message():
    return notificationController().send_push_message()

@app.route('/charge', methods=['GET'])
#@jwt_required    #pushController().send_message()
def charge():
    return chargeController().charge()

@app.route('/salereserve', methods=['POST'])
@jwt_required
def add_sale_reserve():
    return saleController().add_sale_reserve(request)

@app.route('/saleconfirm', methods=['POST'])
@jwt_required
def add_sale_confirm():
    return saleController().add_sale_confirm(request)

@app.route('/saleaccept/<int:index>', methods=['GET'])
@jwt_required
def accept_sale(index):
    return saleController().accept_sale(index)

@app.route('/salerefuse/<int:index>', methods=['GET'])
@jwt_required
def refuse_sale(index):
    return saleController().refuse_sale(index)

@app.route('/salecancel/<int:index>', methods=['GET'])
@jwt_required
def cancel_sale(index):
    return saleController().cancel_sale(index)

@app.route('/sale/<int:index>', methods=['GET'])
@jwt_required
def get_sale_by_id_sale(index):
    return saleController().get_sale_by_id_sale(index)

@app.route('/salecustomer/<int:index>', methods=['GET'])
@jwt_required
def get_sale_by_id_customer(index):
    return saleController().get_sale_by_id_customer(index)

@app.route('/saleuser/<int:index>', methods=['GET'])
@jwt_required
def get_sale_by_id_user(index):
    return saleController().get_sale_by_id_user(index)

@app.route('/coupon/<int:index>', methods=['GET'])
#@jwt_required
def get_customer_coupon_by_id(index):
    return customerController().get_customer_coupon_by_id(index)

@app.route('/dashboardmobile/<int:index>', methods=['GET'])
@jwt_required
def get_dashboard_mobile(index):
    return userController().get_dashboard_mobile(index)

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

@app.route('/wa_login', methods=['GET'])
def wa_login():
    _error = request.args.get('error')
    if _error is None:
        _error = 0
    print(_error)
    return render_template('wa_login.html',error = _error)

@app.route('/wa_login', methods=['POST'])
def wa_login_post():
    _full_name = request.form.get("idTxtUsusario")
    _password = request.form.get("idTxtPassword")
    _entity = userEntity()
    _entity = loginController().login_user_web(_full_name,_password)
    if _entity is None:
        return redirect('/wa_login?error=1')
    else:
        session['full_name'] = _full_name
        return redirect('/wa_list_services')

@app.route('/wa_change_password', methods=['GET'])
def wa_change_password():
    _status = request.args.get('status')
    if _status is None:
        _status = 0
    return render_template('wa_change_password.html',status = _status)

@app.route('/wa_change_password', methods=['POST'])
def wa_change_password_post():
    _full_name = request.form.get("idTxtUsusario")
    _password = request.form.get("idTxtPassword")
    _new_password  = request.form.get("idTxtNewPassword")
    _confirm_password = request.form.get("idTxtConfirmNewPassword")
    _status = 0
    _entity = userEntity()
    _entity = loginController().login_user_web(_full_name,_password)
    if _entity is None:
        _status = 1
    else:
        if _new_password != _confirm_password:
            _status = 2
        else:
            _entity = loginController().change_password_user_web(_full_name,_new_password)
    return redirect('/wa_change_password?status='+str(_status))

@app.route('/wa_logout')
def wa_logout():
   session.pop('full_name', None)
   return redirect('/wa_login')

@app.route('/webadmin', methods=['GET'])
def web_admin():
    return render_template('index.html')

@app.route('/wa_services', methods=['GET'])
def wa_services():
    if  'full_name' in session:
        _id_service = request.args.get('index')
        _entity = None
        if _id_service is not None:
            _entity = serviceController().get_service_by_id_wa(_id_service)
        return render_template('wa_services.html', service = _entity)
    else:
        return redirect('/wa_login')

@app.route('/wa_services', methods=['POST'])
def wa_services_post():
    if  'full_name' in session:
        _entity = serviceEntity()
        _entity.full_name = request.form["idTxtFullName"]
        _entity.color = request.form["idtxtColor"]
        _entity.id = request.form.get("idtxtService")
        _status = request.form.get("idSlEstado")
        if _entity.id is None:
            if request.files:
                image = request.files["idFileImage"]
                path_image = os.path.join(app.config["IMAGE_UPLOADS"], image.filename)
                image.save(path_image) 
                with open(path_image,"rb") as f:
                    _file_image=f.read()
                    _entity.file_image = _file_image
            serviceController().add_service(_entity)
        else:
            serviceController().update_service(_entity,_status)
            if request.files and request.files.get("idFileImage") is not None :
                image = request.files["idFileImage"]
                if image.filename:
                    path_image = os.path.join(app.config["IMAGE_UPLOADS"], image.filename)
                    image.save(path_image) 
                    with open(path_image,"rb") as f:
                        _file_image=f.read()
                    serviceController().update_file_image(_entity.id,_file_image)
        return redirect('/wa_list_services')
    else:
        return redirect('/wa_login')

@app.route('/wa_list_services', methods=['GET'])
def wa_list_services():
    if  'full_name' in session:
        _data_services = serviceController().get_services_wa()
        return render_template('wa_list_services.html',data_services = _data_services)
    else:
        return redirect('/wa_login')

@app.route('/wa_list_sub_services', methods=['GET'])
def wa_list_sub_services():
    if  'full_name' in session:
        _id_service = request.args.get("iSlServicio")
        if _id_service is None:
            _id_service = 0
        print(_id_service)
        _data_sub_services = serviceController().get_sub_services_wa(_id_service)
        _data_services = serviceController().get_services_wa()
        return render_template('wa_list_sub_services.html',data_sub_services = _data_sub_services, data_services= _data_services)
    else:
        return redirect('/wa_login')

@app.route('/wa_sub_services', methods=['GET'])
def wa_sub_services():
    if  'full_name' in session:
        _id_sub_customer = request.args.get('index')
        _entity = None
        _data_services = serviceController().get_services_wa()
        if _id_sub_customer is not None:
            print(_id_sub_customer)
            _entity = serviceController().get_sub_service_by_id_wa(_id_sub_customer)
        return render_template('wa_sub_services.html', sub_service = _entity, data_services= _data_services)
    else:
        return redirect('/wa_login')

@app.route('/wa_sub_services', methods=['POST'])
def wa_sub_services_post():
    if  'full_name' in session:
        _entity = subServiceEntity()
        _entity.id = request.form.get("idtxtSubService")
        _id_service = request.form.get("iSlServicio")
        _entity.full_name = request.form.get("idTxtFullName")
        _entity.in_filter = request.form.get("idSlEnFiltro")
        _status = request.form.get("idSlEstado")
        if _entity.id is None:
            serviceController().add_sub_service(_entity,_id_service,_status)
        else:
            serviceController().update_sub_service(_entity,_id_service,_status)
        return redirect('/wa_list_sub_services')
    else:
        return redirect('/wa_login')

@app.route('/wa_dashboard', methods=['GET'])
def wa_dashboard():
    if  'full_name' in session:
        _dashboardEntity = dashboardEntity()
        _data_dashboard_services = []
        _dashboardEntity = userController().get_dashboard_general()
        if _dashboardEntity is None:
            _dashboardEntity = dashboardEntity()
        _dashboardEntity.classToFormat()
        _data_dashboard_services = userController().get_dashboard_service()
        return render_template('wa_dashboard.html',dashboardEntity = _dashboardEntity,data_dashboard_services = _data_dashboard_services )
    else:
        return redirect('/wa_login')
        
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
                serviceController().update_file_image(1,z)                        
            return redirect(request.url)
    return render_template("upload_image.html")
    
    #uploadController().get()
    #uploadController().implicit()

@app.route('/wa_list_users', methods=['GET'])
def wa_list_users():
    if  'full_name' in session:
        _users = userController().get_users_wa()
        return render_template('wa_list_users.html', data_users = _users)
    else:
        return redirect('/wa_login')

@app.route('/wa_user_status', methods=['GET'])
def wa_user_status():
    if  'full_name' in session:
        _id_user = request.args.get('index')
        _status = request.args.get('status')
        print(_status)
        if _status == '1':
            userController().confirm_user_status(_id_user)
        if _status == '3':
            print(3)
            userController().refuse_user_status(_id_user)
        return render_template('wa_user_status.html',status = _status)
    else:
        return redirect('/wa_login')

@app.route('/wa_push_notification', methods=['GET'])
def wa_push_notification():
    if  'full_name' in session:
        _status = request.args.get('status')
        return render_template('wa_push_notification.html',status = _status)
    else:
        return redirect('/wa_login')

@app.route('/wa_push_notification', methods=['POST'])
def wa_push_notification_post():
    if  'full_name' in session:
        _id_destination= request.form.get("iSlDestino")
        _message = request.form.get("idTxtMensaje")
        notificationController().send_notifiacion_message(_id_destination,_message)
        _status = 1
        return redirect('/wa_push_notification?status='+str(_status))
    else:
        return redirect('/wa_login')

@app.route('/wa_coupon', methods=['GET'])
def wa_coupon():
    if  'full_name' in session:
        _status = userController().get_coupon_status_wa()
        return render_template('wa_coupon.html',status = _status)
    else:
        return redirect('/wa_login')

@app.route('/wa_coupon', methods=['POST'])
def wa_coupon_post():
    if  'full_name' in session:
        _status= request.form.get("iSlEstado")
        userController().update_coupon_status_wa(_status)
        return redirect('/wa_coupon')
    else:
        return redirect('/wa_login')


@app.route('/desencriptar', methods=['GET'])
def get_desencriptar():
    claseen = AESCipher('3DD9D7132A079527BDBA1A0F29D47FB7')
    ecriptado = claseen.encrypt('411111111111111')
    print(ecriptado)
    num = claseen.decrypt(ecriptado)
    print(num)
    return '1'

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)

