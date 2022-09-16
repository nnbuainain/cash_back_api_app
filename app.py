from flask import Flask, jsonify
from flask_restful import Resource, Api
from models.costumer import CostumerModel
from resources.costumer import Costumers, Costumer, CostumerRegister
from models.product import ProductModel
from resources.product import Products, Product, ProductRegister
from models.sale import SaleModel
from resources.sale import Sales, Sale, SaleRegister
from models.cashback import CashBackModel
from resources.cashback import CashBacks, CashBack, CashBackRegister
from resources.user import User, UserRegister, UserLogin, UserLogout
from flask_jwt_extended import JWTManager
from blacklist import BLACKLIST


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] =  'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] =  False
app.config['JWT_SECRET_KEY'] = 'DontTellAnyone'
app.config['JWT_BLACKLIST_ENABLED'] = True


api = Api(app)
jwt = JWTManager(app)


@app.before_first_request
def create_database():
    database.create_all()

@jwt.token_in_blocklist_loader
def check_blacklist(self, token):
    return token['jti'] in BLACKLIST

@jwt.revoked_token_loader
def access_token_invalidated(jwt_header, jwt_payload):
    return jsonify({"message" : "You've been logged out"}), 401 #unauthorized



api.add_resource(User, '/users/<int:user_id>')
api.add_resource(UserRegister, '/register_user')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')
api.add_resource(Costumers, '/costumers/')
api.add_resource(Costumer, '/costumers/<string:costumer_id_cpf>')
api.add_resource(CostumerRegister, '/register_costumer')
api.add_resource(Products, '/products/')
api.add_resource(Product, '/products/<int:id>')
api.add_resource(ProductRegister, '/register_product')
api.add_resource(Sales, '/sales')
api.add_resource(Sale, '/sales/<int:sale_id>')
api.add_resource(SaleRegister, '/register_sale')
api.add_resource(CashBacks, '/cashbacks')
api.add_resource(CashBack, '/cashbacks/<int:cashback_id>')
api.add_resource(CashBackRegister, '/register_cashback')


if __name__ == '__main__':
    from sql_alchemy import database
    database.init_app(app)
    app.run(host = '0.0.0.0', debug = True)