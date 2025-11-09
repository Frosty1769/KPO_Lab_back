import uuid
from flask import jsonify, session
from db import db
from model.model import Characters, SpellInv, Spells, WeaponInv, Weapons
from schemas.characters import CharUpd
from schemas.spell import Spell
from schemas.weapon import Weapon


def char_list():
    chars = db.session.query(Characters).filter(Characters.id_user == session.get('id')).all()
    
    _res = [{"id": char.id_public, "name": char.name, "lvl": char.lvl, "class_type": char.class_type} for char in chars]
    
    return jsonify({"status": "ok", "data": _res})

def char_add(char_name, user_id):
    _id_public = uuid.uuid4()

    print(user_id)

    db.session.add(Characters(id_public = str(_id_public), name = char_name, id_user = user_id))
    db.session.commit()
    
    return jsonify({"status": "ok", "data": None})

def char_info(char_id):
    _char = db.session.query(Characters).filter(Characters.id_public == char_id).first()
    if not _char:
        return jsonify({"status": "error", "message": "Персонаж не найден"})
    
    _res = {}
    _res['id'] = _char.id_public
    _res['name'] = _char.name
    _res['class_type'] = _char.class_type
    _res['race'] = _char.race
    _res['background'] = _char.background
    _res['alignment'] = _char.alignment

    _res['lvl'] = _char.lvl
    _res['exp'] = _char.exp

    _res['armor'] = _char.armor
    _res['initiative'] = _char.initiative
    _res['speed'] = _char.speed
    _res['insp'] = _char.insp
    _res['def_bonus'] = _char.def_bonus

    _res['money'] = {"gold": _char.gold, "silver": _char.silver, "bronze": _char.bronze,}
    _res['death'] = {"pos": _char.death_pos, "neg": _char.death_neg}

    _hp = {"value": _char.hp, "max_hp": _char.max_hp, "temp_hp": _char.temp_hp}

    _all_char_weapons = db.session.query(WeaponInv).filter(WeaponInv.id_char == _char.id_public).all()
    _weapons = []
    for weapon_item in _all_char_weapons:
        _weapon_base = db.session.query(Weapons).filter(Weapons.id == weapon_item.id_weapon).first()
        if not _weapon_base:
            db.session.delete(weapon_item)
            db.session.commit()
            continue
        _weapon_base_dict = Weapon(**_weapon_base.__dict__)
        _weapons.append({'id': weapon_item.id, **(_weapon_base_dict.model_dump())})
    
    _all_char_spells = db.session.query(SpellInv).filter(SpellInv.id_char == _char.id_public).all()
    _spells = []
    for spell_item in _all_char_spells:
        _spell_base = db.session.query(Spells).filter(Spells.id == spell_item.id_spell).first()
        if not _spell_base:
            db.session.delete(spell_item)
            db.session.commit()
            continue
        _spell_base_dict = Spell(**_spell_base.__dict__)
        _spells.append({'id': spell_item.id, **(_spell_base_dict.model_dump())})

    _attrs = {}
    _attrs['str'] = {"name": "str", "value": _char.str, "mod": _char.mod_str}
    _attrs['dex'] = {"name": "dex", "value": _char.dex, "mod": _char.mod_dex}
    _attrs['end'] = {"name": "end", "value": _char.end, "mod": _char.mod_end}
    _attrs['int'] = {"name": "int", "value": _char.int, "mod": _char.mod_int}
    _attrs['wis'] = {"name": "wis", "value": _char.wis, "mod": _char.mod_wis}
    _attrs['cha'] = {"name": "cha", "value": _char.cha, "mod": _char.mod_cha}

    _perks = {}
    _perks['acrobatics'] = {"value": _char.is_acrobatics, "mod": _char.acrobatics, 'name': 'acrobatics'}
    _perks['animal_handling'] = {"value": _char.is_animal_handling, "mod": _char.animal_handling, 'name': 'animal_handling'}
    _perks['arcana'] = {"value": _char.is_arcana, "mod": _char.arcana, 'name': 'arcana'}
    _perks['athletics'] = {"value": _char.is_athletics, "mod": _char.athletics, 'name': 'athletics'}
    _perks['deception'] = {"value": _char.is_deception, "mod": _char.deception, 'name': 'deception'}
    _perks['history'] = {"value": _char.is_history, "mod": _char.history, 'name': 'history'}
    _perks['insight'] = {"value": _char.is_insight, "mod": _char.insight, 'name': 'insight'}
    _perks['intimidation'] = {"value": _char.is_intimidation, "mod": _char.intimidation, 'name': 'intimidation'}
    _perks['investigation'] = {"value": _char.is_investigation, "mod": _char.investigation, 'name': 'investigation'}
    _perks['medicine'] = {"value": _char.is_medicine, "mod": _char.medicine, 'name': 'medicine'}
    _perks['nature'] = {"value": _char.is_nature, "mod": _char.nature, 'name': 'nature'}
    _perks['perception'] = {"value": _char.is_perception, "mod": _char.perception, 'name': 'perception'}
    _perks['performance'] = {"value": _char.is_performance, "mod": _char.performance, 'name': 'performance'}
    _perks['persuasion'] = {"value": _char.is_persuasion, "mod": _char.persuasion, 'name': 'persuasion'}
    _perks['religion'] = {"value": _char.is_religion, "mod": _char.religion, 'name': 'religion'}
    _perks['sleight_of_hand'] = {"value": _char.is_sleight_of_hand, "mod": _char.sleight_of_hand, 'name': 'sleight_of_hand'}
    _perks['stealth'] = {"value": _char.is_stealth, "mod": _char.stealth, 'name': 'stealth'}
    _perks['survival'] = {"value": _char.is_survival, "mod": _char.survival, 'name': 'survival'}

    _res['hp'] = _hp
    _res['attrs'] = _attrs
    _res['perks'] = _perks
    _res['weapons'] = _weapons
    _res['spells'] = _spells

    return jsonify({"status": "ok", "data": _res})

def char_update(char_id, args: CharUpd) -> None:
    _char = db.session.query(Characters).filter(char_id == Characters.id_public).first()
    _char.class_type = args.class_type
    _char.race = args.race
    _char.background = args.background
    _char.alignment = args.alignment
    _char.lvl = args.lvl
    _char.exp = args.exp

    _char.death_pos = args.death.pos
    _char.death_neg = args.death.neg

    _char.armor = args.armor
    _char.initiative = args.initiative
    _char.speed = args.speed
    _char.insp = args.insp
    _char.def_bonus = args.def_bonus
    
    _char.hp = args.hp.value
    _char.max_hp = args.hp.max_hp
    _char.temp_hp = args.hp.temp_hp

    _char.str = args.attrs.str.value
    _char.dex = args.attrs.dex.value
    _char.end = args.attrs.end.value
    _char.int = args.attrs.int.value
    _char.wis = args.attrs.wis.value
    _char.cha = args.attrs.cha.value
    _char.mod_str = args.attrs.str.mod
    _char.mod_dex = args.attrs.dex.mod
    _char.mod_end = args.attrs.end.mod
    _char.mod_int = args.attrs.int.mod
    _char.mod_wis = args.attrs.wis.mod
    _char.mod_cha = args.attrs.cha.mod

    _char.class_type = args.class_type
    _char.class_type = args.class_type
    _char.class_type = args.class_type
    _char.class_type = args.class_type

    _char.gold = args.money.gold
    _char.silver = args.money.silver
    _char.bronze = args.money.bronze

    _char.acrobatics = args.perks.acrobatics.mod
    _char.animal_handling = args.perks.animal_handling.mod
    _char.arcana = args.perks.arcana.mod
    _char.athletics = args.perks.athletics.mod
    _char.deception = args.perks.deception.mod
    _char.history = args.perks.history.mod
    _char.insight = args.perks.insight.mod
    _char.intimidation = args.perks.intimidation.mod
    _char.investigation = args.perks.investigation.mod
    _char.medicine = args.perks.medicine.mod
    _char.nature = args.perks.nature.mod
    _char.perception = args.perks.perception.mod
    _char.performance = args.perks.performance.mod
    _char.persuasion = args.perks.persuasion.mod
    _char.religion = args.perks.religion.mod
    _char.sleight_of_hand = args.perks.sleight_of_hand.mod
    _char.stealth = args.perks.stealth.mod
    _char.survival = args.perks.survival.mod

    _char.is_acrobatics = args.perks.acrobatics.value
    _char.is_animal_handling = args.perks.animal_handling.value
    _char.is_arcana = args.perks.arcana.value
    _char.is_athletics = args.perks.athletics.value
    _char.is_deception = args.perks.deception.value
    _char.is_history = args.perks.history.value
    _char.is_insight = args.perks.insight.value
    _char.is_intimidation = args.perks.intimidation.value
    _char.is_investigation = args.perks.investigation.value
    _char.is_medicine = args.perks.medicine.value
    _char.is_nature = args.perks.nature.value
    _char.is_perception = args.perks.perception.value
    _char.is_performance = args.perks.performance.value
    _char.is_persuasion = args.perks.persuasion.value
    _char.is_religion = args.perks.religion.value
    _char.is_sleight_of_hand = args.perks.sleight_of_hand.value
    _char.is_stealth = args.perks.stealth.value
    _char.is_survival = args.perks.survival.value

    db.session.commit()

    return jsonify({"status": 'ok', 'data': None})
    
# (id_public,                                  id_user, name, class_type, race, background, alignment, lvl, exp, death_pos, death_neg, armor, initiative, speed, insp, def_bonus, hp, max_hp, temp_hp, str, dex, "end", int, wis, cha, mod_str, mod_dex, mod_end, mod_int, mod_wis, mod_cha, gold, silver, bronze, acrobatics, animal_handling, arcana, athletics, deception, history, insight, intimidation, investigation, medicine, nature, perception, performance, persuasion, religion, sleight_of_hand, stealth, survival, is_acrobatics, is_animal_handling, is_arcana, is_athletics, is_deception, is_history, is_insight, is_intimidation, is_investigation, is_medicine, is_nature, is_perception, is_performance, is_persuasion, is_religion, is_sleight_of_hand, is_stealth, is_survival)
# (UUID('26123f8e-cf91-49c8-9da7-ac3e73033e99'), 1, 'new', 'fighter', 'human', 'outlander', 'neutral_good', 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0