from flask import Flask
from flask_restful import Resource, Api
    
app = Flask(__name__)

api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] =  'sqlite:///banco.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] =  False

@app.before_first_request
def cria_banco():
    banco.create_all()


if __name__ == '__main__':
    from sqlalchemy import banco
    banco.init_app(app)
    app.run(debug = True)