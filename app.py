from flask import Flask
from flask_restful import Api
from db import db

app = Flask(__name__)
api = Api(app)

@app.before_first_request
def create_all():
    db.create_tables()

api.add_resource(Itemlist, "/items")
api.add_resource(Item, "/item/<string:name>")
api.add_resource(User, "/register")
api.add_resource(Store,"/store/<string:name>")
api.add_resource(StoreList,"/stores")

if __name__ == "__main__":
    app.run(debig=True)