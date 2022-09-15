from flask_restful import Resource, reqparse
from models.product import ProductModel

attributes = reqparse.RequestParser()
attributes.add_argument('category', type = str, required = True, help = "Please inform a valid product's category")
attributes.add_argument('value', type = float, required = True, help = "Please inform a valid product's value")


class Products(Resource):
    def get(self):
        return {'products' : [product.to_json() for product in ProductModel.query.all()]}


class Product(Resource):
    product_categories = ['A', 'B', 'C']
    
    def get(self, id: int):
        product = ProductModel.find_product(id)

        if product:
            return product.to_json()
        
        return {'message' : 'Product not found'}, 404 # Bad Request
    

    def delete(self, id : int):
        product = ProductModel.find_product(id)

        if product:
            try:
                product.delete()
                return {'message' : "Product with id '{}' successfully deleted".format(id)}
            
            except:
                return {'message' : 'An internal error has occurred while deleting product'}, 500 # Internal Server Error
        
        return {'message' : 'Product not found'}
            

class ProductRegister(Resource):   
    def post(self):
        data = attributes.parse_args()
        
        if data['category'].upper() not in Product.product_categories:
            return {'message' : "Product Category must be one of the following '{}'. ".format(Product.product_categories)}
        
        if type(data['value']) is not float or data['value'] < 0:
            return {'message' : 'Invalid Product value, product value must be a positive decimal value'}

        try:
            product = ProductModel(**data)
            product.save()
        
        except:
            return {'message' : 'An internal error has occurred while saving product'}, 500 # Internal Server Error
    
        return {'message' : "Product with id '{}' successfully registered".format(product.id)}