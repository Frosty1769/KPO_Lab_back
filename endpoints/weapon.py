from flask import Blueprint, request, session
from flask_restx import Api, Resource
from db_actions.weapons import weapon_add, weapon_add_char, weapon_delete_char, weapon_list_all

from schemas.weapon import Weapon

bp = Blueprint("weapon", __name__)
api = Api(bp, default="weapon", default_label="weapon")

class WeaponAdd(Resource):
    def post(self):
        _data = request.json
        _data = Weapon(**_data)
        return weapon_add(_data)
    
class WeaponList(Resource):
    def get(self):
        return weapon_list_all()
    
class WeaponAddChar(Resource):
    def post(self, _id_char):
        _data = request.json
        return weapon_add_char(_data, _id_char)
    
class WeaponDeleteChar(Resource):
    def delete(self, _id_item):
        return weapon_delete_char(_id_item)
    
api.add_resource(WeaponAdd, '/weapons/add')
api.add_resource(WeaponList, '/weapons')
api.add_resource(WeaponAddChar, '/character/weapon/<_id_char>')
api.add_resource(WeaponDeleteChar, '/character/weapon/<_id_item>')