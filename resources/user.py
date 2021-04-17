from flask_restful import Resource, reqparse
from models.user import UserModel
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token

user_parser = reqparse.RequestParser()
user_parser.add_argument("username",
                    type=str,
                    required=True,
                    help="This Field is required"
                    )
user_parser.add_argument("password",
                    type=str,
                    required=True,
                    help="This Field is required"
                    )

class UserRegister(Resource):
    def post(self):
        data = user_parser.parse_args()

        if UserModel.find_by_username(data["username"]):
            return {"message": "User with username Already Exists"}, 400
        user = UserModel(**data)
        user.save_to_db()
        return {"message": "User Created Successfully"}, 201

class User(Resource):
    @classmethod    #Since we dont need to access object of this class we can make classmethod
    def get(cls,user_id):
        user = UserModel.find_by_userid(user_id)
        if user:
            return user.json()
        return {"message": "User Not Found"},404

    @classmethod
    def delete(cls,user_id):
        user = UserModel.find_by_userid(user_id)
        if user:
            user.delete_from_db()
            return {"message": "User deleted Successfully"}
        return {"message": "User Not Found"},404

class UserLogin(Resource):
    def post(self):
        data = user_parser.parse_args()
        user = UserModel.find_by_username(data["username"])
        if user and check_password_hash(user.password, data["password"]):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {
                "access_token": access_token,
                "refresh_token": refresh_token
                }
        return {"message": "Invalid user credentials"}, 401