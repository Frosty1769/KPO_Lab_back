from db import db
from sqlalchemy.dialects.sqlite import TEXT, INTEGER, REAL
from datetime import datetime


class User(db.Model):
    """
    Таблица пользователей: администраторы и кассиры
    """
    __tablename__ = 'users'
    
    id = db.Column(INTEGER, autoincrement=True, primary_key=True, nullable=False)
    username = db.Column(TEXT, nullable=False, unique=True)
    password = db.Column(TEXT, nullable=False)
    role = db.Column(TEXT, nullable=False)  # 'admin' или 'cashier'
    created_at = db.Column(TEXT, default=lambda: datetime.utcnow().isoformat())

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'role': self.role,
            'created_at': self.created_at
        }
    
    def __repr__(self):
        return f"<User {self.username} ({self.role})>"


class Product(db.Model):
    """
    Таблица товаров на складе
    """
    __tablename__ = 'products'
    
    id = db.Column(INTEGER, autoincrement=True, primary_key=True, nullable=False)
    article = db.Column(TEXT, nullable=False, unique=True)  # артикул (уникальный)
    name = db.Column(TEXT, nullable=False)
    price = db.Column(REAL, nullable=False)  # цена за единицу
    quantity = db.Column(INTEGER, nullable=False, default=0)  # количество на складе
    created_at = db.Column(TEXT, default=lambda: datetime.utcnow().isoformat())
    updated_at = db.Column(TEXT, default=lambda: datetime.utcnow().isoformat(), onupdate=lambda: datetime.utcnow().isoformat())

    def to_dict(self):
        return {
            'id': self.id,
            'article': self.article,
            'name': self.name,
            'price': self.price,
            'quantity': self.quantity,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    
    def __repr__(self):
        return f"<Product {self.article}: {self.name} ({self.quantity} шт.)>"


class SoldProduct(db.Model):
    """
    История проданных товаров
    """
    __tablename__ = 'sold_products'
    
    id = db.Column(INTEGER, autoincrement=True, primary_key=True, nullable=False)
    article = db.Column(TEXT, nullable=False)  # артикул товара
    name = db.Column(TEXT, nullable=False)     # название на момент продажи
    price = db.Column(REAL, nullable=False)    # цена на момент продажи
    quantity = db.Column(INTEGER, nullable=False)  # проданное количество
    total_amount = db.Column(REAL, nullable=False)  # общая сумма (price * quantity)
    sold_at = db.Column(TEXT, default=lambda: datetime.utcnow().isoformat())  # дата и время продажи

    def to_dict(self):
        return {
            'id': self.id,
            'article': self.article,
            'name': self.name,
            'price': self.price,
            'quantity': self.quantity,
            'total_amount': self.total_amount,
            'sold_at': self.sold_at
        }
    
    def __repr__(self):
        return f"<SoldProduct {self.article}: {self.quantity} шт. на сумму {self.total_amount} руб.)>"

