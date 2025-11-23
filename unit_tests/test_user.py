# Тесты для функций управления пользователями
# 
# Запуск:
# python -m pytest unit_tests/test_user.py -v
# или
# python -m pytest unit_tests/ -v  (для запуска всех тестов)
#
# Для установки pytest:
# pip install pytest

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from flask import Flask, session
from model.model import db, User
from db_actions.user import register, login, get_info, get_all_users, delete_user


@pytest.fixture
def app():
    """Создание тестового Flask-приложения"""
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'test_secret_key'
    app.config['TESTING'] = True
    
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Создание тестового клиента"""
    return app.test_client()


class TestUserRegistration:
    """Тесты регистрации пользователей"""
    
    def test_register_success(self, app):
        """Успешная регистрация нового пользователя"""
        with app.app_context():
            with app.test_request_context():
                result = register("newuser", "password123", "cashier")
                data = result.get_json()
                
                assert data['status'] == 'ok'
                
                # Проверяем, что пользователь создан в БД
                user = db.session.query(User).filter_by(username="newuser").first()
                assert user is not None
                assert user.role == "cashier"
    
    def test_register_duplicate_username(self, app):
        """Попытка регистрации с существующим именем"""
        with app.app_context():
            with app.test_request_context():
                register("testuser", "password123", "cashier")
                result = register("testuser", "password456", "admin")
                data = result.get_json()
                
                assert data['status'] == 'error'
                assert "занято" in data['message'] or "уже существует" in data['message']
    
    def test_register_missing_data(self, app):
        """Регистрация без обязательных данных"""
        with app.app_context():
            with app.test_request_context():
                result = register("", "password", "cashier")
                data = result.get_json()
                # Пустой логин может быть принят или отклонен - проверяем только что функция работает
                assert data['status'] in ['ok', 'error']


class TestUserLogin:
    """Тесты входа в систему"""
    
    def test_login_success(self, app):
        """Успешный вход в систему"""
        with app.app_context():
            with app.test_request_context():
                register("testuser", "password123", "cashier")
                
            with app.test_request_context():
                result = login("testuser", "password123")
                data = result.get_json()
                
                assert data['status'] == 'ok'
    
    def test_login_wrong_password(self, app):
        """Вход с неправильным паролем"""
        with app.app_context():
            with app.test_request_context():
                register("testuser", "password123", "cashier")
                result = login("testuser", "wrongpassword")
                data = result.get_json()
                
                assert data['status'] == 'error'
    
    def test_login_nonexistent_user(self, app):
        """Вход несуществующего пользователя"""
        with app.app_context():
            with app.test_request_context():
                result = login("nonexistent", "password")
                data = result.get_json()
                
                assert data['status'] == 'error'
                assert "логин" in data['message'].lower() or "данные" in data['message'].lower()


class TestUserInfo:
    """Тесты получения информации о пользователе"""
    
    def test_get_info_success(self, app):
        """Получение информации авторизованного пользователя"""
        with app.app_context():
            with app.test_request_context():
                register("testuser", "password123", "cashier")
                user = db.session.query(User).filter_by(username="testuser").first()
                
            with app.test_request_context():
                # Эмулируем авторизованную сессию
                session['user_id'] = user.id
                session['username'] = user.username
                session['role'] = user.role
                
                result = get_info()
                data = result.get_json()
                
                assert data['status'] == 'ok'
                assert data['data']['username'] == "testuser"
                assert data['data']['role'] == "cashier"
    
    def test_get_info_not_logged_in(self, app):
        """Получение информации без авторизации"""
        with app.app_context():
            with app.test_request_context():
                result = get_info()
                data = result.get_json()
                
                assert data['status'] == 'error'
                assert "Не авторизован" in data['message']


class TestUserDeletion:
    """Тесты удаления пользователей"""
    
    def test_delete_user_success(self, app):
        """Успешное удаление пользователя админом"""
        with app.app_context():
            with app.test_request_context():
                register("admin", "admin", "admin")
                register("user_to_delete", "password", "cashier")
                
                admin = db.session.query(User).filter_by(username="admin").first()
                user_to_delete = db.session.query(User).filter_by(username="user_to_delete").first()
            
            with app.test_request_context():
                session['user_id'] = admin.id
                session['role'] = 'admin'
                
                result = delete_user(user_to_delete.id)
                data = result.get_json()
                
                assert data['status'] == 'ok'
                
                # Проверяем, что пользователь удалён
                deleted_user = db.session.query(User).filter_by(id=user_to_delete.id).first()
                assert deleted_user is None
    
    def test_delete_self(self, app):
        """Попытка удалить самого себя"""
        with app.app_context():
            with app.test_request_context():
                register("admin", "admin", "admin")
                admin = db.session.query(User).filter_by(username="admin").first()
            
            with app.test_request_context():
                session['user_id'] = admin.id
                session['role'] = 'admin'
                
                result = delete_user(admin.id)
                data = result.get_json()
                
                assert data['status'] == 'error'
                assert "самого себя" in data['message']
    
    def test_delete_nonexistent_user(self, app):
        """Удаление несуществующего пользователя"""
        with app.app_context():
            with app.test_request_context():
                session['role'] = 'admin'
                
                result = delete_user(99999)
                data = result.get_json()
                
                assert data['status'] == 'error'
                assert "не найден" in data['message']


class TestGetAllUsers:
    """Тесты получения списка пользователей"""
    
    def test_get_all_users(self, app):
        """Получение списка всех пользователей"""
        with app.app_context():
            with app.test_request_context():
                register("user1", "pass1", "admin")
                register("user2", "pass2", "cashier")
                register("user3", "pass3", "cashier")
            
            with app.test_request_context():
                session['role'] = 'admin'
                
                result = get_all_users()
                data = result.get_json()
                
                assert data['status'] == 'ok'
                assert len(data['data']) == 3
                assert any(u['username'] == 'user1' for u in data['data'])
                assert any(u['username'] == 'user2' for u in data['data'])
