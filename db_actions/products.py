from flask import jsonify, session
from db import db
from model.model import Product
from sqlalchemy.exc import IntegrityError


def add_product(article, name, price, quantity=0):
    """
    Добавление товара на склад или увеличение количества существующего
    Только для администратора
    """
    print(f"[DEBUG] Session data: {dict(session)}")  # Отладка
    print(f"[DEBUG] Role from session: {session.get('role')}")  # Отладка
    
    if session.get('role') != 'admin':
        return jsonify({"status": "error", "message": "Доступ запрещён"})
    
    try:
        # Используем SERIALIZABLE изоляцию для безопасности
        db.session.connection(execution_options={'isolation_level': 'SERIALIZABLE'})
        
        existing_product = db.session.query(Product).filter(Product.article == article).with_for_update().first()
        
        if existing_product:
            # Товар уже существует - увеличиваем количество
            existing_product.quantity += quantity
            db.session.commit()
            return jsonify({
                "status": "ok", 
                "message": "Количество товара обновлено",
                "data": existing_product.to_dict()
            })
        else:
            # Создаём новый товар
            new_product = Product(article=article, name=name, price=price, quantity=quantity)
            db.session.add(new_product)
            db.session.commit()
            return jsonify({
                "status": "ok", 
                "message": "Товар добавлен",
                "data": new_product.to_dict()
            })
    except IntegrityError:
        db.session.rollback()
        return jsonify({"status": "error", "message": "Ошибка при добавлении товара"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": f"Ошибка: {str(e)}"})


def get_all_products():
    """
    Получение всех товаров на складе
    """
    products = db.session.query(Product).all()
    return jsonify({
        "status": "ok",
        "data": [product.to_dict() for product in products]
    })


def get_product_by_article(article):
    """
    Получение товара по артикулу
    """
    product = db.session.query(Product).filter(Product.article == article).first()
    
    if not product:
        return jsonify({"status": "error", "message": "Товар не найден"})
    
    return jsonify({
        "status": "ok",
        "data": product.to_dict()
    })


def update_product_quantity(article, quantity_delta):
    """
    Изменение количества товара (может быть положительным или отрицательным)
    Используется при продаже товаров
    """
    try:
        db.session.connection(execution_options={'isolation_level': 'SERIALIZABLE'})
        
        product = db.session.query(Product).filter(Product.article == article).with_for_update().first()
        
        if not product:
            db.session.rollback()
            return jsonify({"status": "error", "message": "Товар не найден"})
        
        new_quantity = product.quantity + quantity_delta
        
        if new_quantity < 0:
            db.session.rollback()
            return jsonify({"status": "error", "message": "Недостаточно товара на складе"})
        
        product.quantity = new_quantity
        db.session.commit()
        
        return jsonify({
            "status": "ok",
            "data": product.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": f"Ошибка: {str(e)}"})


def process_sale(items):
    """
    Обработка продажи (списание товаров со склада)
    items: список словарей вида [{"article": "ART001", "quantity": 2}, ...]
    """
    try:
        db.session.connection(execution_options={'isolation_level': 'SERIALIZABLE'})
        
        total_price = 0
        processed_items = []
        
        for item in items:
            article = item.get('article')
            quantity = item.get('quantity')
            
            if not article or not quantity or quantity <= 0:
                db.session.rollback()
                return jsonify({"status": "error", "message": "Некорректные данные товара"})
            
            product = db.session.query(Product).filter(Product.article == article).with_for_update().first()
            
            if not product:
                db.session.rollback()
                return jsonify({"status": "error", "message": f"Товар {article} не найден"})
            
            if product.quantity < quantity:
                db.session.rollback()
                return jsonify({
                    "status": "error", 
                    "message": f"Недостаточно товара {product.name} на складе. Доступно: {product.quantity}"
                })
            
            # Списываем товар
            product.quantity -= quantity
            item_total = product.price * quantity
            total_price += item_total
            
            processed_items.append({
                "article": product.article,
                "name": product.name,
                "price": product.price,
                "quantity": quantity,
                "total": item_total
            })
        
        db.session.commit()
        
        return jsonify({
            "status": "ok",
            "message": "Продажа завершена",
            "data": {
                "items": processed_items,
                "total_price": total_price
            }
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": f"Ошибка при обработке продажи: {str(e)}"})


def delete_product(article):
    """
    Удаление товара (только для админа)
    """
    if session.get('role') != 'admin':
        return jsonify({"status": "error", "message": "Доступ запрещён"})
    
    try:
        product = db.session.query(Product).filter(Product.article == article).first()
        
        if not product:
            return jsonify({"status": "error", "message": "Товар не найден"})
        
        db.session.delete(product)
        db.session.commit()
        
        return jsonify({"status": "ok", "message": "Товар удалён"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": f"Ошибка: {str(e)}"})
