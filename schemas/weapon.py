from enums.weapon_spell import AttackType, DamageType, HoldType
from schemas.characters import MyBaseModel


class Weapon(MyBaseModel):
    name: str
    hold_type: HoldType
    attack_type: AttackType
    damage: str
    damage_type: DamageType    
    range: int
