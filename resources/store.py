from os import name
from sqlalchemy import delete
from models.store import StoreModel
from flask_restful import Resource

class Store(Resource):

    def post(self, name):
        check = StoreModel.search_store(name)
        if check:
            return {"message": "The store {} already exists, please make a new store".format(name)}

        store = StoreModel(name)
        store.save_to_db()
        return store.json(), 200
        
    
    def delete(self, name):
        search = StoreModel.search_store(name)
        if search:
            search.delete_from_db()
            return {"message": "the store {} has been deleted".format(name)}
        
        return {"message":"the store you searched for cannot be found"}

    def get(self, name):
        store = StoreModel.search_store(name)
        if not store:
            return {"message": "The store {} does not exists please search for an existing store".format(name)}

        return store.json(), 200

class Stores(Resource):

    def get(self):
        return {'stores': list(map(lambda x: x.json(), StoreModel.query.all()))}


        
       
        
