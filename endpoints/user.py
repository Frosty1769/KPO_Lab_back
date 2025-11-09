from flask import Blueprint, request, session
from flask_restx import Api, Resource 
from db_actions.user import _info, login, logout, register

bp = Blueprint("user", __name__)
api = Api(bp, default="user", default_label="user")

class UserLogin(Resource):
    def post(self):
        username = request.json.get('username')
        password = request.json.get('password')
        return login(username, password)

class UserRegister(Resource):
    def post(self):
        username = request.json.get('username')
        password = request.json.get('password')
        return register(username, password)

class UserInfo(Resource):
    def get(self):
        return _info(session.get('id_public'),session.get('name'),session.get('role'))

class UserLogout(Resource):
    def post(self):
        return logout()

api.add_resource(UserLogin, "/login")
api.add_resource(UserRegister, "/register")
api.add_resource(UserInfo, "/info")
api.add_resource(UserLogout, "/logout")