from db import db

class ItemModel:
    __tablename__ = "items" #Table for this model
    id = db.Column(db.Integer, primary_key=True)    #defining columns of table
    name = db.Column(db.String(50))
    price = db.Column(db.Float(precision=2))

    store_id = db.Column(db.Integer,db.ForeignKey("stores.id")) #creating a column using Foreign Key
    store = db.relationship("StoreModel")   #Specifying Relationship

    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id =store_id

    def json(self):
        return {"name": self.name, "price": self.price} #custoom method to return json form of object

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first() #filtering table with name and taking first value

    def save_to_db(self):
        db.session.add(self) #Inserting into table, updates if already present
        db.session.commit() #commiting changes to the database
    
    def delete_from_db(self):
        db.session.delete(self) #Deleting from table using object
        db.session.commit()     #commiting deleted changes