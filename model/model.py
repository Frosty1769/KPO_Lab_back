from db import db
from sqlalchemy.dialects.sqlite import TEXT, INTEGER, BOOLEAN
from sqlalchemy.sql.schema import ForeignKey
import sqlalchemy as sa

from enums.weapon_spell import AttackType, DamageType, HoldType, SpellType


class Users(db.Model):
    id = db.Column(INTEGER,autoincrement=True, primary_key=True, nullable=False)
    id_public = db.Column(TEXT(32), nullable=False)
    username = db.Column(TEXT, nullable=False, unique=True)
    password = db.Column(TEXT, nullable=False) 

class Characters(db.Model):
    id = db.Column(INTEGER,autoincrement=True, primary_key=True, nullable=False)
    id_public = db.Column(TEXT(32), nullable=False)
    id_user = db.Column(INTEGER, ForeignKey("users.id"), nullable=False)

    name = db.Column(TEXT, nullable=False)
    class_type = db.Column(TEXT, nullable=False, default="fighter") 
    race = db.Column(TEXT, nullable=False, default='human') 
    background = db.Column(TEXT, nullable=False, default='outlander') 
    alignment = db.Column(TEXT, nullable=False, default='neutral_good') 
    lvl = db.Column(INTEGER, nullable=False, default=1) 
    exp = db.Column(INTEGER, nullable=False, default=0) 

    
    death_pos = db.Column(INTEGER, nullable=False, default=0) 
    death_neg = db.Column(INTEGER, nullable=False, default=0) 

    armor = db.Column(INTEGER, nullable=False, default=0) 
    initiative = db.Column(INTEGER, nullable=False, default=0) 
    speed = db.Column(INTEGER, nullable=False, default=0) 
    insp = db.Column(INTEGER, nullable=False, default=0) 
    def_bonus = db.Column(INTEGER, nullable=False, default=0) 

    hp = db.Column(INTEGER, nullable=False, default=0) 
    max_hp = db.Column(INTEGER, nullable=False, default=0) 
    temp_hp = db.Column(INTEGER, nullable=False, default=0) 

    str = db.Column(INTEGER, nullable=False, default=0) 
    dex = db.Column(INTEGER, nullable=False, default=0) 
    end = db.Column(INTEGER, nullable=False, default=0) 
    int = db.Column(INTEGER, nullable=False, default=0) 
    wis = db.Column(INTEGER, nullable=False, default=0) 
    cha = db.Column(INTEGER, nullable=False, default=0) 

    mod_str = db.Column(INTEGER, nullable=False, default=0) 
    mod_dex = db.Column(INTEGER, nullable=False, default=0) 
    mod_end = db.Column(INTEGER, nullable=False, default=0) 
    mod_int = db.Column(INTEGER, nullable=False, default=0) 
    mod_wis = db.Column(INTEGER, nullable=False, default=0) 
    mod_cha = db.Column(INTEGER, nullable=False, default=0) 

    gold = db.Column(INTEGER, nullable=False, default=0) 
    silver = db.Column(INTEGER, nullable=False, default=0) 
    bronze = db.Column(INTEGER, nullable=False, default=0) 

    acrobatics = db.Column(INTEGER, nullable=False, default=0) 
    animal_handling = db.Column(INTEGER, nullable=False, default=0) 
    arcana = db.Column(INTEGER, nullable=False, default=0) 
    athletics = db.Column(INTEGER, nullable=False, default=0) 
    deception = db.Column(INTEGER, nullable=False, default=0) 
    history = db.Column(INTEGER, nullable=False, default=0) 
    insight = db.Column(INTEGER, nullable=False, default=0) 
    intimidation = db.Column(INTEGER, nullable=False, default=0) 
    investigation = db.Column(INTEGER, nullable=False, default=0) 
    medicine = db.Column(INTEGER, nullable=False, default=0) 
    nature = db.Column(INTEGER, nullable=False, default=0) 
    perception = db.Column(INTEGER, nullable=False, default=0)
    performance = db.Column(INTEGER, nullable=False, default=0)
    persuasion = db.Column(INTEGER, nullable=False, default=0)
    religion = db.Column(INTEGER, nullable=False, default=0)
    sleight_of_hand = db.Column(INTEGER, nullable=False, default=0)
    stealth = db.Column(INTEGER, nullable=False, default=0)
    survival = db.Column(INTEGER, nullable=False, default=0)

    is_acrobatics = db.Column(BOOLEAN, nullable=False, default=False) 
    is_animal_handling = db.Column(BOOLEAN, nullable=False, default=False) 
    is_arcana = db.Column(BOOLEAN, nullable=False, default=False) 
    is_athletics = db.Column(BOOLEAN, nullable=False, default=False) 
    is_deception = db.Column(BOOLEAN, nullable=False, default=False) 
    is_history = db.Column(BOOLEAN, nullable=False, default=False) 
    is_insight = db.Column(BOOLEAN, nullable=False, default=False) 
    is_intimidation = db.Column(BOOLEAN, nullable=False, default=False) 
    is_investigation = db.Column(BOOLEAN, nullable=False, default=False) 
    is_medicine = db.Column(BOOLEAN, nullable=False, default=False) 
    is_nature = db.Column(BOOLEAN, nullable=False, default=False) 
    is_perception = db.Column(BOOLEAN, nullable=False, default=False)
    is_performance = db.Column(BOOLEAN, nullable=False, default=False)
    is_persuasion = db.Column(BOOLEAN, nullable=False, default=False)
    is_religion = db.Column(BOOLEAN, nullable=False, default=False)
    is_sleight_of_hand = db.Column(BOOLEAN, nullable=False, default=False)
    is_stealth = db.Column(BOOLEAN, nullable=False, default=False)
    is_survival = db.Column(BOOLEAN, nullable=False, default=False)

    

class Weapons(db.Model):
    id = db.Column(TEXT(32), primary_key=True, nullable=False)
    
    name = db.Column(TEXT, nullable=False)

    hold_type = db.Column(sa.Enum(HoldType), nullable=False)
    attack_type = db.Column(sa.Enum(AttackType), nullable=False)
    damage = db.Column(TEXT, nullable=False)
    damage_type = db.Column(sa.Enum(DamageType), nullable=False)
    
    range = db.Column(INTEGER, nullable=False, default = 0)


class Spells(db.Model):
    id = db.Column(TEXT(32), primary_key=True, nullable=False)

    name = db.Column(TEXT, nullable=False)
    type = db.Column(sa.Enum(SpellType), nullable=False)

    attack_type = db.Column(sa.Enum(AttackType), nullable=False)
    damage = db.Column(TEXT, nullable=False)
    damage_type = db.Column(sa.Enum(DamageType), nullable=False)
    
    range = db.Column(INTEGER, nullable=False, default = 0)


class WeaponInv(db.Model):
    id = db.Column(TEXT(32), primary_key=True, nullable=False)
    id_weapon = db.Column(TEXT(32), ForeignKey("weapons.id"),  nullable=False)
    id_char = db.Column(TEXT(32), ForeignKey("characters.id_public"),  nullable=False)

class SpellInv(db.Model):
    id = db.Column(TEXT(32), primary_key=True, nullable=False)
    id_spell = db.Column(TEXT(32), ForeignKey("spells.id"),  nullable=False)
    id_char = db.Column(TEXT(32), ForeignKey("characters.id_public"),  nullable=False)

