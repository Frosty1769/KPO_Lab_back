import uuid
from flask import jsonify, session
from db import db
from model.model import Characters, WeaponInv, Weapons
from schemas.weapon import Weapon

def weapon_add(weapon: Weapon):
    _id = uuid.uuid4()
    db.session.add(Weapons(id =str(_id), **(weapon.model_dump())))
    db.session.commit()

    return jsonify({'status': 'ok', 'data': None})


def weapon_list_all():
    _weapons = db.session.query(Weapons).all()
    _data = []
    for _weapon in _weapons:
        _weaponDict = Weapon(**_weapon.__dict__)
        _data.append({'id': _weapon.id, **(_weaponDict.model_dump())})        
    
    return jsonify({'status': 'ok', 'data': _data})


def weapon_add_char(_data, _id_char):    
    for weapon in _data:
        _id = uuid.uuid4()
        db.session.add(WeaponInv(id=str(_id), id_weapon = weapon['id'], id_char = _id_char))
        
    db.session.commit()

    return jsonify({'status': 'ok', 'data': None})


def weapon_delete_char(_id_item):
    _weapon = db.session.query(WeaponInv).filter(WeaponInv.id == _id_item).first()
    if not _weapon:
        return jsonify({'status': 'error', 'message': "Предмет не найден"})
    db.session.delete(_weapon)
    db.session.commit()
 
    return jsonify({'status': 'ok', 'data': None})