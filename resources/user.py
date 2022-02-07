from multiprocessing import connection
import sqlite3
from tokenize import String
from flask_restful import Resource, reqparse, Api

from models.user import UserModel

class UserRegister(Resource):
    
    # Instantiate an object of parser
    parser = reqparse.RequestParser()
    parser.add_argument('username', type = str, required = True, help = "The username field cannot be left blank")
    parser.add_argument('password', type = str, required = True, help = "The password field cannot be left blank")

    def post(self):
        data = UserRegister.parser.parse_args()

        username = data['username']
        if UserModel.verify_by_username(username):
            return {'message': 'This user already exists'}, 400
        
        user = UserModel(**data)
        user.save_to_db()
        return {'message': 'Account has been created'}, 201



