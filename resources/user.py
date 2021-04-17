from flask_restful import Resource, reqparse
from models.user import UserModel
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt

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
    @classmethod    #Since we dont need object of this class we can make classmethod
    def get(cls,user_id):
        user = UserModel.find_by_userid(user_id)
        if user:
            return user.json()
        return {"message": "User Not Found"},404

    @classmethod
    @jwt_required()
    def delete(cls,user_id):
        claims = get_jwt()  #jwt claims details
        if not claims["is_admin"]:
            #if user claims to be admin then only, he can performs delete operation
            return{"message": "Admin privileges required for this operation"},401
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
            #if user credentials are correct generate access and refresh token
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {
                "access_token": access_token,
                "refresh_token": refresh_token
                }
        return {"message": "Invalid user credentials"}, 401