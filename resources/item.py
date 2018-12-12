import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True, #need a price
        help="This filed cannot be left blank!"
    )
    parser.add_argument('store_id',
        type=int,
        required=True, #need a price
        help="This filed cannot be left blank!"
    )
 
    
    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json(), 200
        return {'message': 'Item not found'}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': "An item with the name '{}' already exists.".format(name)}, 400
        data = Item.parser.parse_args()
        item = ItemModel(name, **data)
        
        try:
            item.upserting()
        except:
            return {'message': 'An error occurred inserting the item'}, 500 

        return item.json(), 201 # 201 has been created
    
    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        """
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        cursor.execute("DELETE FROM items WHERE name = ?", (name,))
        connection.commit()
        connection.close()
 
        """
        return {'message': 'Item deleted'}
    
    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        if not item:
            item = ItemModel(name, **data)
        else:
            item.price = data['price']
        item.upserting()
        return item.json(), 201


class ItemList(Resource):
    def get(self):
        """

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        result = cursor.execute("SELECT * FROM items")
        items = []
        for row in result:
            items.append({'name': row[0], 'price': row[1]})
        connection.close()
        """
        return {'items': [x.json() for x in ItemModel.query.all()]}
        #return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))}
