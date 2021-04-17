from flask_restful import Resource
from models.store import StoreModel
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

class Store(Resource):
    @jwt_required()
    def get(self,name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json(), 200
        return {"message": "Store Not Found"},404
    
    @jwt_required()
    def post(self,name):
        if StoreModel.find_by_name(name):
            return {"message": "Store with {} name already exists".format(name)}, 400

        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            {"messsage": "Error occured while creating store"},500
                
        return store.json(),201
    
    @jwt_required()
    def delete(self,name):
        claims = get_jwt()  #jwt claims details
        if not claims["is_admin"]:
            #if user claims to be admin then only, he can performs delete operation
            return{"message": "Admin privileges required for this operation"},401
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
            return {"message": "Store Deleted"}, 200
        return {"message": "Store doesnot exist"}, 404


class StoreList(Resource):
    @jwt_required(optional=True)    #seting jwt Token optional
    def get(self):
        userid = get_jwt_identity() #function gives currrently logged in user's details
        stores = StoreModel.find_all()
        if userid:
            #if user is logged in complete store details are sent else only store names
            return {"stores": [store.json() for store in stores]}, 200
        return {
            "stores": [store.name for store in stores],
            "message": "Please login to see more details"
            }, 200
