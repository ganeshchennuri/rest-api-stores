from flask_restful import Resource,reqparse
from models.item import ItemModel
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity

class Item(Resource):
    parser = reqparse.RequestParser() #Parsing the body using reqparse
    parser.add_argument("price",
        type=float,
        required=True,
        help="This Field cannot be empty"
        )
    parser.add_argument("store_id",
        type=int,
        required=True,
        help="store id is required"
        )

    @jwt_required()
    def get(self,name):
        try:
            item = ItemModel.find_by_name(name)
            if item:
                return item.json()
            return {"message": "item not found"},404
        except:
            return {"message": "Error while fetching item details"}, 500

    def post(self,name):
        if ItemModel.find_by_name(name):
            return {"message": "An item with {} name already exists".format(name)}

        data = Item.parser.parse_args()
        item = ItemModel(name,**data)
        try:
            item.save_to_db()
        except:
            return {"message": "Error while inserting item"}, 500
        return item.json(),201

    def put(self,name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name,**data)
        else:
            item.price = data['price']
            
        item.save_to_db()
        return item.json()

    @jwt_required()
    def delete(self,name):
        claims = get_jwt()  #jwt claims details
        if not claims["is_admin"]:
            #if user claims to be admin then only, he can performs delete operation
            return{"message": "Admin privileges required for this operation"},401

        item = ItemModel.find_by_name(name)
        if item is None:
            return {"message": "Item not found"},404
        item.delete_from_db()
        return {"message": "item deleted successfully"}


class Itemlist(Resource):
    @jwt_required(optional=True)    #seting jwt Token optional
    def get(self):
        userid = get_jwt_identity() #function gives currrently logged in user's details if any
        items = ItemModel.find_all()
        if userid:
            return {"items": [item.json() for item in items]}   #if user is logged in complete item details are sent else only item names
        return {
            "items": [item.name for item in items],
            "message": "Please login to see more details"
            }