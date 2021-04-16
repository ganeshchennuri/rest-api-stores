from flask_restful import Resource,reqparse
from models.item import ItemModel

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

    def get(self, name):
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

    def delete(self,name):
        item = ItemModel.find_by_name(name)
        if item is None:
            return {"message": "Item not found"},404
        item.delete_from_db()
        return {"message": "item deleted successfully"}


class Itemlist(Resource):
    def get(self):
        return {"items": [item.json() for item in ItemModel.find_all()]}
