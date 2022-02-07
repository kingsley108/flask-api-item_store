from multiprocessing import connection
from flask_restful import Resource, reqparse
from flask_jwt import JWT, jwt_required
from models.item import ItemModel



class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type = float, required = True, 
    help = "This field cannot be left blank")
    parser.add_argument('store_id', type = str,required = True, help = "Enter a store before you send this request")

    def get(self, name):
        item = ItemModel.search_item(name)
        if item:
            return item.json()

        return {"message": "item could not be found"}, 404


    def post(self, name):
        if ItemModel.search_item(name):
            return {"message": f"The resource with the name {name} already exists"}
        
        data = Item.parser.parse_args()
        item = ItemModel(name, **data)

        try:
           item.save_to_db()
        except:
            return {"message": "A server error has occured"}, 500
        
        # Save item in the database
        return item.json()
    
    def delete(self, name):
        item = ItemModel.search_item(name)
        if item:
            item.delete_from_db()
            return {"message": f"The resource with the name {name} has been deleted"}
            
        return {"message": f"The resource with the name {name} does not exist"}
        
    def put(self, name):
        data = Item.parser.parse_args()
        price = data['price']
        item = ItemModel.search_item(name)
        # if the name exits we update the field
        if item:
            try:
                item = ItemModel(name, **data)
                item.save_to_db()
            except:

                return {"message": "A server error has occured"}, 500
        else:  
            try:
                item.price = data['price']
                item.store_id  = data['store_id']

            except:
                return {"message": "A server error has occured"}, 500    

        return item.json()

# 201 is the status code saying things are okay and it has CREATED a resource, 
# this is for POST request
# 404 is the status code from the browser saying the resource was not found
# 200 is the status code from the browser saying everything is ok and it has created a resource.
# Status code 400 is for bad request
# 500 is internal server error.

class Items(Resource):
    def get(self):
        items = ItemModel.query.all()
        return {"items": [item.json() for item in items]}

