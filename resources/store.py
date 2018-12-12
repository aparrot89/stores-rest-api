from flask_restful import Resource
from models.store import StoreModel

class Store(Resource):
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json() # defaut 200
        return {'message': 'Store not found'}, 404
    
    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'message' : 'The store "{}" already exist'.format(name)}, 400
        store = StoreModel(name)
        try:
            store.upserting()
        except:
            return {'message': 'An error occur while creating the store'}, 500
        return store.json(), 201

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
        return {'message': 'A store was deleted'}


class StoreList(Resource):
    def get(self):
        return {'stores': [store.json() for store in StoreModel.query.all()]}
