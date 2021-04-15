class UserModel:
    __tablename__ = "users"
    id = db.column(db.Integer, primary_key=True)
    name = db.column(db.String(50),nullable=False)
    password = db.column(db.string(200))

    def __init__(self, username, password):
        self.username = username
        self.password = password
    
    @classmethod
    def find_by_username(cls,username):
        return cls.query.filter_by(username=username).first()
        
    @classmethod
    def find_by_userid(cls,_id): #Querying table with userid filter
        return cls.query.filter_by(id=_id).first()
    
    def save_to_db(self):
        db.session.add(self)    #Adding users to Database
        db.session.commit()