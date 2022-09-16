from flask_restful import Resource, reqparse
from models.user import UserModel
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
#from hmac import compare_digest
from blacklist import BLACKLIST
from werkzeug.security import generate_password_hash, check_password_hash

attributes = reqparse.RequestParser()
attributes.add_argument('login', type = str, required = True, help = "the field 'login' cannot be blank")
attributes.add_argument('password', type = str, required = True, help = "the field 'password' cannot be blank")


class User(Resource):

    @jwt_required()
    def get(self, user_id):
        user = UserModel.find_user(user_id)        
        
        if user:
            return user.to_json()
        
        return {'message': 'User not found.'}, 404 #not found

    @jwt_required()
    def delete(self, user_id):
        user = UserModel.find_user(user_id)
        
        if user:
            try:
                user.delete_user()
            
            except:
                return {"message" : "an internal error occurred while saving user"}, 500

            return {"message":"User '{}' deleted".format(user_id)}
        
        return {'message':'User not found'}


class UserRegister(Resource):
    
    def post(self):  
        data = attributes.parse_args()
        
        if UserModel.find_user_by_login(data['login']):
            return {"message" : "Login '{}' already exists".format(data['login'])}
        
        user = UserModel(data['login'], generate_password_hash(data['password']))
        user.save_user()

        return {'message' : 'User registered successfully'}

class UserLogin(Resource):
    
    @classmethod
    def post(cls):
        data = attributes.parse_args()
        
        user = UserModel.find_user_by_login(data['login'])

        if user and check_password_hash(user.password, data['password']):
            access_token = create_access_token(identity= user.user_id)
            return {'access_token' : access_token}
        
        return {'message' : 'Incorrect login or password'}

class UserLogout(Resource):

    @jwt_required()
    def post(self):
        jwt_id = get_jwt()['jti'] # JWT TOKEN IDENTIFIER
        
        BLACKLIST.add(jwt_id)
        
        return {'message' : 'You successfully logged out'}


