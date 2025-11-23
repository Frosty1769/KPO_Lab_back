# Тесты для моделей данных
# 
# Запуск:
# python -m pytest unit_tests/test_models.py -v
# или
# python -m pytest unit_tests/ -v  (для запуска всех тестов)
#
# Для установки pytest:
# pip install pytest

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from flask import Flask
from model.model import db, User, Product, SoldProduct


@pytest.fixture
def app():
    """Создание тестового Flask-приложения"""
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['TESTING'] = True
    
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


class TestUserModel:
    """Тесты модели User"""
    
    def test_user_to_dict(self, app):
        """Проверка метода to_dict() для User"""
        with app.app_context():
            user = User(
                username="testuser",
                password="hashed_password",
                role="cashier",
                created_at="2024-01-15T10:30:00"
            )
            db.session.add(user)
            db.session.commit()
            
            result = user.to_dict()
            
            assert result['id'] is not None
            assert result['username'] == "testuser"
            assert result['role'] == "cashier"
            assert result['created_at'] == "2024-01-15T10:30:00"
            assert 'password' not in result  # Пароль не должен возвращаться
    
    def test_user_repr(self, app):
        """Проверка строкового представления User"""
        with app.app_context():
            user = User(username="admin", role="admin", password="pass")
            db.session.add(user)
            db.session.commit()
            assert repr(user) == "<User admin (admin)>"


class TestProductModel:
    """Тесты модели Product"""
    
    def test_product_to_dict(self, app):
        """Проверка метода to_dict() для Product"""
        with app.app_context():
            product = Product(
                article="ART001",
                name="Молоко",
                price=89.90,
                quantity=50,
                created_at="2024-01-15T10:30:00",
                updated_at="2024-01-15T11:00:00"
            )
            db.session.add(product)
            db.session.commit()
            
            result = product.to_dict()
            
            assert result['id'] is not None
            assert result['article'] == "ART001"
            assert result['name'] == "Молоко"
            assert result['price'] == 89.90
            assert result['quantity'] == 50
            assert result['created_at'] == "2024-01-15T10:30:00"
            assert result['updated_at'] == "2024-01-15T11:00:00"
    
    def test_product_repr(self, app):
        """Проверка строкового представления Product"""
        with app.app_context():
            product = Product(article="ART001", name="Молоко", quantity=50, price=89.90)
            db.session.add(product)
            db.session.commit()
            assert repr(product) == "<Product ART001: Молоко (50 шт.)>"


class TestSoldProductModel:
    """Тесты модели SoldProduct"""
    
    def test_sold_product_to_dict(self, app):
        """Проверка метода to_dict() для SoldProduct"""
        with app.app_context():
            sold = SoldProduct(
                article="ART001",
                name="Молоко",
                price=89.90,
                quantity=2,
                total_amount=179.80,
                sold_at="2024-01-15T12:00:00"
            )
            db.session.add(sold)
            db.session.commit()
            
            result = sold.to_dict()
            
            assert result['id'] is not None
            assert result['article'] == "ART001"
            assert result['name'] == "Молоко"
            assert result['price'] == 89.90
            assert result['quantity'] == 2
            assert result['total_amount'] == 179.80
            assert result['sold_at'] == "2024-01-15T12:00:00"
    
    def test_sold_product_repr(self, app):
        """Проверка строкового представления SoldProduct"""
        with app.app_context():
            sold = SoldProduct(article="ART001", quantity=2, total_amount=179.80, name="Молоко", price=89.90)
            db.session.add(sold)
            db.session.commit()
            assert repr(sold) == "<SoldProduct ART001: 2 шт. на сумму 179.8 руб.)>"
