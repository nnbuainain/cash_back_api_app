from flask_restful import Resource, reqparse
from models.costumer import CostumerModel
from models.product import ProductModel
from models.sale import SaleModel
from flask_jwt_extended import jwt_required

attributes = reqparse.RequestParser()
attributes.add_argument('costumer_id_cpf', type = str, required = True, help = "Please inform a valid costumer id")
attributes.add_argument('products_and_quantities', type = dict, action = "append", required = True, help = "Please inform a valid product dictionary")


class Sales(Resource):
    
    @jwt_required()
    def get(self):
        return {'sales' : [sale.to_json() for sale in SaleModel.query.all()]}


class Sale(Resource):
    
    @jwt_required()
    def get(self, sale_id: int):
        sale = SaleModel.find_sale(sale_id)

        if sale:
            return sale.to_json()
        
        return {'message' : 'Sale not found'}, 404 # Bad Request
    
    @jwt_required()
    def delete(self, sale_id : int):
        sale = SaleModel.find_sale(sale_id)

        if sale:
            try:
                sale.delete()
                return {'message' : "Sale with id '{}' successfully deleted".format(sale_id)}
            
            except:
                return {'message' : 'An internal error has occurred while deleting sale'}, 500 # Internal Server Error
        
        return {'message' : 'Sale not found'}


class SaleRegister(Resource):   
    products = []
    
    @jwt_required()
    def post(self):
        data = attributes.parse_args()

        if CostumerModel.find_costumer(data['costumer_id_cpf']):
            for requested_product in data['products_and_quantities']:
                
                if type(requested_product['quantity']) is not int or requested_product['quantity'] < 1:
                    return {"message" : "Invalid product quantity. Needs to be a number greater than 0"}, 404 # Bad Request

                product = ProductModel.find_product(requested_product['id'])                
                if not product:
                    return {"message": "The product with id '{}' is not registered in the database".format(requested_product['id'])}, 404 # Bad Request

                product_json = product.to_json()
                product_json.update(quantity = requested_product['quantity'])            
                
                SaleRegister.products.append(product_json)
                
            try:
                sale = SaleModel(data['costumer_id_cpf'], SaleRegister.products)
                sale.save()

                SaleRegister.products.clear()
                
                return sale.to_json(), 201 # CREATED
            
            except:
                return {'message' : 'An internal error has occurred while saving sale'}, 500 # Internal Server Error
                

        return {'message' : 'Costumer not registered in the database'}