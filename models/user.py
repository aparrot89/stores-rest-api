from db import db
# model = internal representation of an entity
# whereas, resource = external representation of an entity
#                   = the client doe not interact directly with it

class UserModel(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))
    
    def __init__(self, username, password):
        self.username = username
        self.password = password
    
    def upserting(self):
        db.session.add(self)
        db.session.commit()
    
    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()
        """
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        
        query = "SELECT * FROM users WHERE username=?"
        result = cursor.execute(query, (username, )) # always in the forms of a tuple!
        # on peut iterer ou recuper une ligne, si pas de ligne => row == None
        row = result.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None
        connection.close()
        return user
            """ 

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
        """
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        
        query = "SELECT * FROM users WHERE id=?"
        result = cursor.execute(query, (_id, )) # always in the forms of a tuple!
        # on peut iterer ou recuper une ligne, si pas de ligne => row == None
        row = result.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None
        connection.close()
        return user
        """
