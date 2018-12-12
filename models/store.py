from db import db

class StoreModel(db.Model):
    __tablename__ = 'stores'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    
    # back reference, list
    # to see which items are in the items database or item table
    # which the store id equal to its own id
    # lazy dynamic mean when it will be loaded, only when self.items.all() is called
    items = db.relationship('ItemModel', lazy='dynamic')

    def __init__(self, name):
        self.name = name

    def json(self):
        # avec lazy='dynamic' => self.items is a querybuild which may be request in the future
        return {'name': self.name, 'items':[item.json() for item in self.items.all()]}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def upserting(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
