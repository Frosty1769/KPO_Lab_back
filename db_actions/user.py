import uuid
from flask import jsonify, session
from db import db
from model.model import Users

def register(username, password):
    _newby = db.session.query(Users).filter(Users.username == username).first()
    
    if _newby:
        return jsonify({"status": "error", "message": "Имя занято"})

    _uuid = uuid.uuid4()
    db.session.add(Users(id_public=str(_uuid), username=username, password=password))
    db.session.commit()
    
    return jsonify({"status": "ok"})
    


def login(username, password):
    _user = db.session.query(Users).filter(Users.username == username).first()

    if not _user:
        return jsonify({"status": "error", "message": "Неправильный логин"})
    if not _user.password == password:
        return jsonify({"status": "error", "message": "Неправильный пароль"})
    
    session["id"] = _user.id
    session["id_public"] = _user.id_public
    session["name"] = _user.username
    session["role"] = 'admin'

    return jsonify({"status": "ok", "data": {"id" : str(_user.id_public), "name" : _user.username, "role" : 'admin', 'isAdmin' : True}})

def _info(_id_public, _name, _role):
    return jsonify({"status": "ok", "data": {"id" : str(_id_public) if _id_public else None , "name" : _name, "role" : _role, 'isAdmin' : True}})

def logout():
    session.pop('id', None)
    session.pop('id_public', None)
    session.pop('name', None)
    session.pop('role', None)
    return jsonify({"status": "ok"})

