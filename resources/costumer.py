from flask_restful import Resource, reqparse
from models.costumer import CostumerModel

attributes = reqparse.RequestParser()
attributes.add_argument('costumer_id_cpf', type = str, required = True, help = "Please inform costumer's id")
attributes.add_argument('name', type = str)

class Costumer(Resource):
    def get(self, costumer_id_cpf):
        costumer = CostumerModel.find_costumer(costumer_id_cpf)

        if costumer:
            return costumer.to_json()
        
        return {'message' : 'User not found'}, 404 # Bad Request

class CostumerRegister(Resource):   
    def post(self):
        data = attributes.parse_args()
        
        if CostumerModel.find_costumer(data['costumer_id_cpf']):
            return {'message'  : 'User id already registered'}
        
        if not len(data.get('costumer_id_cpf')) == 11 or not data.get('costumer_id_cpf').isdecimal():
            return {'message' : 'User id (cpf) must be an 11 digits code containing only numbers'} , 400 # Bad Request

        try:
            costumer = CostumerModel(**data)
            costumer.save()
        
        except:
            return {'message' : 'an internal error has occurred while saving costumer'}, 500
        
        return {'message' : "Costumer with id '{}' successfully created".format(data['costumer_id_cpf'])}



