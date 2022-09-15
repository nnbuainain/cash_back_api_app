from flask_restful import Resource, reqparse
from models.costumer import CostumerModel
from models.product import ProductModel
from models.sale import SaleModel

attributes = reqparse.RequestParser()
attributes.add_argument('costumer_id_cpf', type = str, required = True, help = "Please inform a valid costumer id")
attributes.add_argument('products_and_quantities', type = dict, action = "append", required = True, help = "Please inform a valid product dictionary")


class Sales(Resource):
    def get(self):
        return {'sales' : [sale.to_json() for sale in SaleModel.query.all()]}

class Sale(Resource):
    def get(self, sale_id):
        sale = SaleModel.find_sale(sale_id)

        if sale:
            return sale.to_json()
        
        return {'message' : 'Sale not found'}, 404 # Bad Request
    
    def delete(self, sale_id : int):
        sale = SaleModel.find_sale(sale_id)

        if sale:
            sale.delete()
            return {'message' : "Sale with id '{}' successfully deleted".format(sale_id)}
        
        return {'message' : 'Sale not found'}
            
class SaleRegister(Resource):   
    products = []
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
                
            sale = SaleModel(data['costumer_id_cpf'], SaleRegister.products)
            sale.save()

            SaleRegister.products.clear()
            
            return sale.to_json(), 201 # CREATED
                

        return {'message' : 'Costumer not registered in the database'}