from flask_restful import Resource, reqparse
from models.costumer import CostumerModel
from models.product import ProductModel
from models.sale import SaleModel
from models.cashback import CashBackModel
from requests import request
from flask_jwt_extended import jwt_required
import json


CASHBACK_URL = 'https://5efb30ac80d8170016f7613d.mockapi.io/api/mock/Cashback'
HEADER = {'Content-Type' : 'application/json'}

attributes = reqparse.RequestParser()
attributes.add_argument('sale_id', type = int)
class CashBacks(Resource):
    @jwt_required()
    def get(self):
        return {'cashbacks' : [cashback.to_json() for cashback in CashBackModel.query.all()]}

class CashBack(Resource):
    @jwt_required()
    def get(self, cashback_id: int):
        cashback = CashBackModel.find_cashback(cashback_id)

        if cashback:
            return cashback.to_json()
        
        return {'message' : 'Cashback not found'}, 404 # Bad Request
    
    @jwt_required()
    def delete(self, cashback_id : int):
        cashback = CashBackModel.find_cashback(cashback_id)

        if cashback:
            try:
                cashback.delete()
                return {'message' : "Cashback with id '{}' successfully deleted".format(cashback_id)}
            except:
                return {'message' : 'An internal error has occurred while deleting cashback'}, 500 # Internal Server Error
        
        return {'message' : 'Cashback not found'}
            
class CashBackRegister(Resource):   
    cashback_total = 0
    
    @jwt_required()
    def post(self):
        
        sale_id = attributes.parse_args()['sale_id']
        print(sale_id)
        if CashBackModel.find_cashback_by_sale_id(sale_id):
            return {'message' : 'You already cashbacked this sale'}

        sale = SaleModel.find_sale(sale_id).to_json()
        
        if sale:
            for product in sale.get('products'):
                CashBackRegister.cashback_total += product['value'] * product['quantity'] * CashBackRegister.category_percentage(product['category'])
                
            CashBackRegister.cashback_total = round(CashBackRegister.cashback_total,2)
            
            body = {
                "document" : sale['costumer_id_cpf'],
                "cashback" : CashBackRegister.cashback_total
                }
            
            api_response = request('POST', CASHBACK_URL, json = body, headers = HEADER).json()

            cashback = CashBackModel(CashBackRegister.cashback_total, api_response, sale_id)
            
            try:
                cashback.save()

                CashBackRegister.cashback_total = 0

                return cashback.to_json(), 201 # CREATED
            
            except:
                return {'message' : 'An internal error has occurred while saving cashback'}, 500 # Internal Server Error
            
        
    @classmethod
    def category_percentage(cls, category: str):
        category = category.upper()
        
        if category == 'A':
            return 0.03
        
        elif category == 'B':
            return 0.05
        
        elif category == 'C':
            return 0.1

        else:
            return 0                