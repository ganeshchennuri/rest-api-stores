from flask import Flask
from flask_restful import Api

from resources.store import StoreList,Store
from resources.item import Item,Itemlist
from resources.user import UserRegister,User

app = Flask(__name__)   #Initializing Flask Web App

# app.secret_key = 'dejfofioefokeefnkfhjnfefoelnkwkl'
# jwt = JWT(app, authenticate, identity)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'   #configuring sqlite3 with SQLAlchemy
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False    #SQLAlchemy already have modification tracker,turning off FlaskSQLAlchemy event tracker to save resources
app.config["PROPAGATE_EXCEPTIONS"] = True  #Custom exception of other modules like JWT are reflected

api = Api(app)  #converting FaskApp to RESTAPI's

@app.before_first_request   #This method will run before the first request is sent 
def create_tables():
    db.create_all()         #All the necessary tables if not present are created

api.add_resource(Itemlist, "/items")            #creating endpoint for querying all the items
api.add_resource(Item, "/item/<string:name>")   #endpoint for item CRUD operations
api.add_resource(UserRegister, "/register")     #endpoint for Registering the user
api.add_resource(Store,"/store/<string:name>")  #endpoint for addin new stores to the databse
api.add_resource(StoreList,"/stores")           #Querying all the stores details
api.add_resource(User, "/user/<int:user_id>")   #Querying user and deleting user

if __name__ == "__main__":
    from db import db   #Importing here to avoid circular import conflict Since Models also import the db
    db.init_app(app)    #Initializing SQLAlchemy 
    app.run(debug=True) #running our flask application