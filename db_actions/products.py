from flask import jsonify, session
from db import db
from model.model import Product, SoldProduct
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
    Обработка продажи (списание товаров со склада и запись в историю продаж)
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
            
            # Записываем в историю продаж
            sold_product = SoldProduct(
                article=product.article,
                name=product.name,
                price=product.price,
                quantity=quantity,
                total_amount=item_total
            )
            db.session.add(sold_product)
            
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


def get_sales_report():
    """
    Получение отчёта по проданным товарам с группировкой по артикулу
    """
    if session.get('role') != 'admin':
        return jsonify({"status": "error", "message": "Доступ запрещён"})
    
    try:
        # Группируем продажи по артикулу
        from sqlalchemy import func
        
        sales_summary = db.session.query(
            SoldProduct.article,
            SoldProduct.name,
            func.sum(SoldProduct.quantity).label('total_quantity'),
            func.sum(SoldProduct.total_amount).label('total_revenue')
        ).group_by(SoldProduct.article, SoldProduct.name).all()
        
        # Общая выручка
        total_revenue = db.session.query(func.sum(SoldProduct.total_amount)).scalar() or 0
        
        report_data = []
        for sale in sales_summary:
            report_data.append({
                'article': sale.article,
                'name': sale.name,
                'total_quantity': sale.total_quantity,
                'total_revenue': float(sale.total_revenue)
            })
        
        return jsonify({
            "status": "ok",
            "data": {
                "sales": report_data,
                "total_revenue": float(total_revenue)
            }
        })
    except Exception as e:
        return jsonify({"status": "error", "message": f"Ошибка: {str(e)}"})


def clear_sales_history():
    """
    Очистка истории продаж (только для админа)
    """
    if session.get('role') != 'admin':
        return jsonify({"status": "error", "message": "Доступ запрещён"})
    
    try:
        db.session.query(SoldProduct).delete()
        db.session.commit()
        
        return jsonify({"status": "ok", "message": "История продаж очищена"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": f"Ошибка: {str(e)}"})
