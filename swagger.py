from flask import Flask, request
from flask_restx import Api, Resource

app = Flask(__name__)
api = Api(app)

stores = [
    {
        "name" : "My_store",
        "items" :  [{
            "name": "Chair",
            "price" : 100
         }]
    }
]

@api.route('/imisi')
class Home(Resource):
    def get(self):
        return "Hello World" 

@api.route('/store')
class Store(Resource):
    def get(self):
        return {"stores" : stores}
    
@api.route('/store2')
class Dave(Resource):
    def post(self, username):
        if username == "Imisi":
            return "Bankai"
        else:
            return "Loser!"
    
@api.route('/store3')
class Dave(Resource):
    def put(self):
        return "Imisi"
    
@api.route('/store4')
class Dave(Resource):
    def delete(self):
        return "Imisi"


