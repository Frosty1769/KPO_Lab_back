from pydantic import BaseModel

class MyBaseModel(BaseModel):
    class Config:
        pass
        # extra: 'forbid'

class Death(MyBaseModel):
    pos: int
    neg: int

class Hp(MyBaseModel):
    value: int
    max_hp: int
    temp_hp: int

class Attr(MyBaseModel):
    name: str
    value: int
    mod: int

class Attrs(MyBaseModel):
    str: Attr
    dex: Attr
    end: Attr
    int: Attr
    wis: Attr
    cha: Attr

class Money(MyBaseModel):
    gold: int
    silver: int
    bronze: int

class Perk(MyBaseModel):
    name: str
    value: bool
    mod: int

class Perks(MyBaseModel):
    acrobatics: Perk
    animal_handling: Perk
    arcana: Perk
    athletics: Perk
    deception: Perk
    history: Perk
    insight: Perk
    intimidation: Perk
    investigation: Perk
    medicine: Perk
    nature: Perk
    perception: Perk
    performance: Perk
    persuasion: Perk
    religion: Perk
    sleight_of_hand: Perk
    stealth: Perk
    survival: Perk

class CharUpd(MyBaseModel):
    name: str
    class_type: str
    race: str
    background: str 
    alignment: str 
    lvl: int
    exp: int
    
    death: Death

    armor: int
    initiative: int
    speed: int
    insp: int
    def_bonus: int
    hp: Hp
    attrs: Attrs
    money: Money
    perks: Perks
    