from flask_restful import Resource, reqparse
from models.user import UserModel

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("username",
        type=str,
        required=True,
        help="This Field is required"
    )
    parser.add_argument("password",
        type=str,
        required=True,
        help="This Field is required"
    )

    def post(self):
        data = UserRegister.parser.parse_args()

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