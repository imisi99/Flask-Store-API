import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import stores

blp = Blueprint("stores", __name__, description= "Operations on stores")

@blp.route('/store/<string:store_id>')
class Store(MethodView):
    def get(self, store_id):
        try:
            return stores[store_id], 200
        except KeyError:
            abort(404, message = "Store not found.")

    def delete(self, store_id):
        try:
            del stores[store_id]
            return "Store Deleted successfully"
        except KeyError:
            abort(404, message= "Store not found")

    def update(self, store_id):
        store = request.get_data()
        if "name" not in store or "store_id" not in store:
            abort(400, message = "Ensure that you are sending all the required fields")

        try:
            u_store = stores[store_id]
            u_store |= store

            return u_store
        
        except KeyError:
            abort(404, message= "Store not found")

@blp.route('/store')
class StoreList(MethodView):
    def get(self):
        return {'store' : list(stores.values())}, 200

    def post(self):
        store = request.get_json()
        if (
        "name" not in store
        ):
            abort(400, message= "Required fields missing, check that you are sending the: name and price")

        for exist in stores.values():
            if(
                store['name'] == exist['name']
            ):
                abort(400, message= "Already existing Store!")
        store_id = uuid.uuid4().hex
        new_store = {**store, 'id': store_id}
        stores[store_id] = new_store
        return new_store, 201


