from db import db

class StoreModel(db.Model): #Extending db.Model creates mapping between Database and class objects, we can insert, update delete using objects
    __tablename__ = "stores"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    items = db.relationship("ItemModel") #Relationship with ItemModel

    def __init__(self, name):
        self.name = name
    
    def json(self):
        return {
            "id": self.id,
            "name": self.name,
            "items": [item.json() for item in self.items]
            } #json method returns store details and all the items in it

    @classmethod
    def find_by_name(cls,name):
        return cls.query.filter_by(name=name).first() #filters stores ny storename

    def save_to_db(self):
        db.session.add(self)    # adding new store to store table and commiting changes
        db.session.commit()
    
    def delete_from_db(self):
        db.session.delete(self) #Deleting from table using object, commiting 
        db.session.commit()

    @classmethod
    def find_all(cls):
        return cls.query.all()