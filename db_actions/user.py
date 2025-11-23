from flask import jsonify, session
from db import db
from model.model import User
from sqlalchemy.exc import IntegrityError


def register(username, password, role='cashier'):
    """
    Регистрация нового пользователя (кассира или админа)
    """
    try:
        existing_user = db.session.query(User).filter(User.username == username).first()
        
        if existing_user:
            return jsonify({"status": "error", "message": "Имя пользователя занято"})

        new_user = User(username=username, password=password, role=role)
        db.session.add(new_user)
        db.session.commit()
        
        return jsonify({"status": "ok", "message": "Пользователь создан"})
    except IntegrityError:
        db.session.rollback()
        return jsonify({"status": "error", "message": "Ошибка при создании пользователя"})


def login(username, password):
    """
    Аутентификация пользователя
    """
    user = db.session.query(User).filter(User.username == username).first()

    if not user:
        return jsonify({"status": "error", "message": "Неправильный логин"})
    
    if user.password != password:
        return jsonify({"status": "error", "message": "Неправильный пароль"})
    
    # Сохраняем данные в сессию
    session["user_id"] = user.id
    session["username"] = user.username
    session["role"] = user.role

    return jsonify({
        "status": "ok", 
        "data": {
            "id": user.id,
            "username": user.username,
            "role": user.role,
            "isAdmin": user.role == 'admin'
        }
    })


def get_info():
    """
    Получение информации о текущем пользователе
    """
    user_id = session.get('user_id')
    username = session.get('username')
    role = session.get('role')

    if not user_id:
        return jsonify({"status": "error", "message": "Не авторизован"})

    return jsonify({
        "status": "ok", 
        "data": {
            "id": user_id,
            "username": username,
            "role": role,
            "isAdmin": role == 'admin'
        }
    })


def logout():
    """
    Выход из системы
    """
    session.clear()
    return jsonify({"status": "ok", "message": "Вышли из системы"})


def get_all_users():
    """
    Получение списка всех пользователей (только для админа)
    """
    if session.get('role') != 'admin':
        return jsonify({"status": "error", "message": "Доступ запрещён"})
    
    users = db.session.query(User).all()
    return jsonify({
        "status": "ok",
        "data": [user.to_dict() for user in users]
    })


def delete_user(user_id):
    """
    Удаление пользователя (только для админа)
    Нельзя удалить самого себя
    """
    if session.get('role') != 'admin':
        return jsonify({"status": "error", "message": "Доступ запрещён"})
    
    current_user_id = session.get('user_id')
    
    if current_user_id == user_id:
        return jsonify({"status": "error", "message": "Нельзя удалить самого себя"})
    
    try:
        user = db.session.query(User).filter(User.id == user_id).first()
        
        if not user:
            return jsonify({"status": "error", "message": "Пользователь не найден"})
        
        db.session.delete(user)
        db.session.commit()
        
        return jsonify({"status": "ok", "message": "Пользователь удалён"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": f"Ошибка: {str(e)}"})

