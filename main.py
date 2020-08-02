from flask import Flask
from flask import Flask, jsonify, request
from src.models.userModel import userModel
from src.entities.user import userEntity



app = Flask(__name__)

@app.route('/users')
def get_users():
    _user = userEntity('juan','0002')
    print(_user.name +" "+ _user.code )
    return _user.toJSON()

@app.route('/users', methods=['POST'])
def add_user():
    user = userModel()
    print(request.get_json())
    code = user.add_user(request) 
    return {'id': str(code)}, 200

@app.route('/users/<int:index>', methods=['PUT'])
def update_user(index):
    user = userModel()
    _user = user.update_user(request,index) 
    return jsonify(_user), 200

@app.route('/users/<int:index>', methods=['DELETE'])
def delete_user(index):
    user = userModel()
    user.delete_user(index) 
    return 'None', 200

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
    
