import uuid
from flask import jsonify, session
from db import db
from model.model import SpellInv, Spells
from schemas.spell import Spell

def spell_add(spell: Spell):
    _id = uuid.uuid4()
    db.session.add(Spells(id =str(_id), **(spell.model_dump())))
    db.session.commit()

    return jsonify({'status': 'ok', 'data': None})


def spell_list_all():
    _spells = db.session.query(Spells).all()
    _data = []
    for _spell in _spells:
        _spellDict = Spell(**_spell.__dict__)
        _data.append({'id': _spell.id, **(_spellDict.model_dump())})        
    
    return jsonify({'status': 'ok', 'data': _data})


def spell_add_char(_data, _id_char):    
    for spell in _data:
        _id = uuid.uuid4()
        db.session.add(SpellInv(id=str(_id), id_spell = spell['id'], id_char = _id_char))
        
    db.session.commit()

    return jsonify({'status': 'ok', 'data': None})


def spell_delete_char(_id_item):
    _spell = db.session.query(SpellInv).filter(SpellInv.id == _id_item).first()
    if not _spell:
        return jsonify({'status': 'error', 'message': "Предмет не найден"})
    db.session.delete(_spell)
    db.session.commit()
 
    return jsonify({'status': 'ok', 'data': None})