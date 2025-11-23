from flask import Blueprint, request, session
from flask_restx import Api, Resource 
from db_actions.user import get_info, login, logout, register, get_all_users, delete_user

bp = Blueprint("user", __name__)
api = Api(bp, default="user", default_label="Управление пользователями")


class UserLogin(Resource):
    """Аутентификация пользователя"""
    def post(self):
        username = request.json.get('username')
        password = request.json.get('password')
        return login(username, password)


class UserRegister(Resource):
    """Регистрация нового пользователя (кассира)"""
    def post(self):
        username = request.json.get('username')
        password = request.json.get('password')
        role = request.json.get('role', 'cashier')  # По умолчанию кассир
        return register(username, password, role)


class UserInfo(Resource):
    """Получение информации о текущем пользователе"""
    def get(self):
        return get_info()


class UserLogout(Resource):
    """Выход из системы"""
    def post(self):
        return logout()


class UserList(Resource):
    """Список всех пользователей (только для админа)"""
    def get(self):
        return get_all_users()


class UserDelete(Resource):
    """Удаление пользователя (только для админа)"""
    def delete(self, user_id):
        return delete_user(user_id)


api.add_resource(UserLogin, "/login")
api.add_resource(UserRegister, "/register")
api.add_resource(UserInfo, "/info")
api.add_resource(UserLogout, "/logout")
api.add_resource(UserList, "/list")
api.add_resource(UserDelete, "/delete/<int:user_id>")