from db import db

class ItemModel(db.Model):
    __tablename__ = 'items'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))
    
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    store = db.relationship('StoreModel')

    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self):
        return {'name': self.name, 'price':self.price}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()
        # SELECT * FROM __classtable__ WHERE name=name LIMIT 1
        # return a ItemModel object
        """
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()
        if row:
            return cls(*row)
        """

    def upserting(self):
        # as there is a id do the updating or inserting!
        #a session is a collection of object we want to insert
        db.session.add(self)
        db.session.commit()
        """
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        cursor.execute("INSERT INTO items VALUES(?,?)", (self.name, self.price))
        connection.commit()
        connection.close()
        """

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
