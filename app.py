from flask import Flask
from flask_restful import Resource, Api
from models.costumer import CostumerModel
from resources.costumer import Costumers, Costumer, CostumerRegister

app = Flask(__name__)

api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] =  'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] =  False

@app.before_first_request
def create_database():
    database.create_all()

api.add_resource(Costumers, '/costumers/')
api.add_resource(Costumer, '/costumers/<string:costumer_id_cpf>')
api.add_resource(CostumerRegister, '/register_costumer')


if __name__ == '__main__':
    from sql_alchemy import database
    database.init_app(app)
    app.run(debug = True)