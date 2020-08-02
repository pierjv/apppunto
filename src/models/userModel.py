from flask import Flask, jsonify, request

class userModel:

    def get_users(self):
        users = self
        print('get user')
        print(self)
        return users


    def add_user(self,request):
        iduser = 1
        print('add user')
        print(request)
        _user = request.get_json() 
        return iduser

    def update_user(self,request,index):
        print('update user')
        print(request)
        user = request.get_json()
        return user

    def delete_user(self,index):
        print('delete user')
        print(index)
        return 'None'