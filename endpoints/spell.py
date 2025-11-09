from flask import Blueprint, request, session
from flask_restx import Api, Resource
from db_actions.spells import spell_add, spell_add_char, spell_delete_char, spell_list_all

from schemas.spell import Spell

bp = Blueprint("spell", __name__)
api = Api(bp, default="spell", default_label="spell")

class SpellAdd(Resource):
    def post(self):
        _data = request.json
        _data = Spell(**_data)
        return spell_add(_data)
    
class SpellList(Resource):
    def get(self):
        return spell_list_all()
    
class SpellAddChar(Resource):
    def post(self, _id_char):
        _data = request.json
        return spell_add_char(_data, _id_char)
    
class SpellDeleteChar(Resource):
    def delete(self, _id_item):
        return spell_delete_char(_id_item)
    
api.add_resource(SpellAdd, '/spells/add')
api.add_resource(SpellList, '/spells')
api.add_resource(SpellAddChar, '/character/spell/<_id_char>')
api.add_resource(SpellDeleteChar, '/character/spell/<_id_item>')