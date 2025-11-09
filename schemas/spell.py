from enums.weapon_spell import AttackType, DamageType, HoldType, SpellType
from schemas.characters import MyBaseModel


class Spell(MyBaseModel):
    name: str
    type: SpellType
    
    attack_type: AttackType
    damage: str
    damage_type: DamageType    

    range: int
