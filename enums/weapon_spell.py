from enum import Enum
class DamageType(str, Enum):
    ACID = 'acid'
    BLUNT = 'blunt'
    COLD = 'cold'
    FIRE = 'fire'
    FORCE = 'force'
    LIGHTNING = 'lightning'
    NECROTIC = 'necrotic'
    PIERCE = 'pierce'
    POISON = 'poison'
    PSYCHIC = 'psychic'
    RADIANT = 'radiant'
    SLASH = 'slash' 
    THUNDER = 'thunder' 

class AttackType(str, Enum):
    MELEE = 'melee'
    RANGED = 'ranged'

class HoldType(str, Enum):
    TWOHAND = 'twohand'
    ONEHAND = 'onehand'

class SpellType(str, Enum):
    SPELL = 'spell'
    CHARM = 'charm'
