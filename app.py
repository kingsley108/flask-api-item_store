from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, Items
from db import db
from resources.store import Store, Stores

app = Flask(__name__)
db.init_app(app)
app.secret_key = 'jose'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
api = Api(app)
jwt = JWT(app, authenticate, identity)

# Terneray operator -> if item is not None else 404

@app.before_first_request
def create_tables():
    db.create_all()
    
api.add_resource(Items, "/items")
api.add_resource(Store, "/store/<string:name>")
api.add_resource(Stores, "/stores")
api.add_resource(UserRegister, "/register")
api.add_resource(Item, "/item/<string:name>")

# Ony runs the app if we are running the app file directly and not running
# by another file importing it.
if __name__ == '__main__' :
    app.run(port= 5000)
