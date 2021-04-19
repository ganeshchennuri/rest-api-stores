from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager

from resources.store import StoreList, Store
from resources.item import Item, Itemlist
from resources.user import UserRegister, User, UserLogin, UserLogout, TokenRefresh
from blacklist import BLACKLIST

app = Flask(__name__)   #Initializing Flask Web App

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'   #configuring sqlite3 with SQLAlchemy
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False    #SQLAlchemy already have modification tracker,turning off FlaskSQLAlchemy event tracker to save resources
app.config["PROPAGATE_EXCEPTIONS"] = True               #Custom exception of other modules like JWT are reflected
app.config["JWT_BLACKLIST_ENABLED"] = True
app.config["JWT_BLACKLIST_TOKEN_CHECKS"] = ["access", "refresh"]

app.secret_key = 'dejfofioefokeefnkfhjnfefoelnkwkl' #Secret key to encrypt flask app (servcer side encryption)
api = Api(app)  #converting FaskApp to RESTAPI's

jwt = JWTManager(app)
#app.config["JWT_SECRET_KEY"] = "qwertyuipxvvxvswkjoubnemxxnekijebxnxjbshllazxb"  #Secret key to jwt tokens

@jwt.additional_claims_loader   # attaching claims data to each jwt payload, usecase access level control
def add_claims_to_jwt(identity):
    if identity == 1:           #hardcoing the admin check, we can import froma config or db
        return {"is_admin": True}
    return {"is_admin": False}

#This method will check if a token is blacklisted, and will be called automatically when blacklist is enabled
@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(jwt_header,jwt_data):
    #returns True if blocklisted else False
    return jwt_data['jti'] in BLACKLIST

#The following callbacks are used for customizing jwt response/error messages.
@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_data):
    return {
        "description": "Token has been revoked",
        "error": "token_revoked"
    }, 401

api.add_resource(Itemlist, "/items")            #creating endpoint for querying all the items
api.add_resource(Item, "/item/<string:name>")   #endpoint for item CRUD operations
api.add_resource(UserRegister, "/register")     #endpoint for Registering the user
api.add_resource(Store,"/store/<string:name>")  #endpoint for addin new stores to the databse
api.add_resource(StoreList,"/stores")           #Querying all the stores details
api.add_resource(User, "/user/<int:user_id>")   #Querying user and deleting user
api.add_resource(UserLogin, "/login")           #User logi and JWT access token generation
api.add_resource(TokenRefresh, "/refresh")      #token refresh endpoint, takes refresh and provides access token
api.add_resource(UserLogout, "/logout")          #logout endpoint

if __name__ == "__main__":
    from db import db   #Importing here to avoid circular import conflict Since Models also import the db
    db.init_app(app)    #Initializing SQLAlchemy 
    app.run(port=5000,debug=False) #running our flask application