from flask import Flask
from flask import Flask, jsonify, request
from src.models.userModel import userModel
from src.entities.userEntity import userEntity
from src.controllers.userController import userController
from src.cn.data_base_connection import Database


app = Flask(__name__)

@app.route('/users', methods=['GET'])
def get_users():
    return userController().get_users()

@app.route('/users', methods=['POST'])
def add_user():
    return userController().add_user(request)

@app.route('/users/<int:index>', methods=['PUT'])
def update_user(index):
    return userController().update_user(request,index)

@app.route('/users/<int:index>', methods=['DELETE'])
def delete_user(index):
    return userController().delete_user(index)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)

