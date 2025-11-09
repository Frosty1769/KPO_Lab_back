from flask import Blueprint, request, session
from flask_restx import Api, Resource
from db_actions.characters import char_add, char_info, char_list, char_update
from schemas.characters import CharUpd 

bp = Blueprint("character", __name__)
api = Api(bp, default="character", default_label="character")

class CharacterList(Resource):
    def get(self):
        return char_list()
    
class CharacterAdd(Resource):
    def post(self):
        _name = request.json.get('name')
        return char_add( _name, session.get('id'))
    
class CharacterInfo(Resource):
    def get(self, _char_id):
        return char_info(_char_id)
    
class CharacterUpdate(Resource):
    def post(self, _char_id):
        _data = request.json
        _data = CharUpd(**_data)
        return char_update(_char_id, _data)
    
api.add_resource(CharacterList, "/player")
api.add_resource(CharacterAdd, "/player/add")
api.add_resource(CharacterInfo, "/character/<_char_id>")
api.add_resource(CharacterUpdate, "/character/<_char_id>")