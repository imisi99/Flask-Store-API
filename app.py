from flask import Flask, request
from flask_smorest import abort
from db import *
import uuid


app = Flask(__name__)

@app.get('/')
def Landing():
    return "Welcome to my first Flask api"

# @app.get('/store', methods= ["POST"])
# def check():
#     data = request.json
#     username = data.get('username', '')
#     if username == 'Imisioluwa23':
#         return store
#     else:
#         return "Intruder alert"

@app.get('/store')
def get_all_store():
    return {'store' : list(stores.values())}, 200


@app.get('/item')
def get_all_item():
    return {"item" : list(item.values())}, 200


@app.post('/store')
def create_store():
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

@app.post('/item')
def create_item():
    store = request.get_json()
    if ('name' not in store
        or 'price' not in store):
        abort(400, message= "Bad Request ensure that you are sending all the required information")

    for exist in item.values():
        if(store['name'] == exist['name']):
            abort(400, message= 'Name already in use!')
    
    item_id = uuid.uuid4().hex
    new_item = {**store, 'id' : item_id}
    item[item_id] = new_item

    return new_item, 201
    

@app.get("/store/<string:store_id>")
def get_store(store_id):
    try:
        return stores[store_id], 200
    except KeyError:
        abort(404, message = "Store not found.")

@app.get("/item/<string:item_id>")
def get_item(item_id):
    try:
        return item[item_id], 200
    except KeyError:
        abort(404, message = "Item not found.")

@app.put('/store/<string:store_id>')
def update_store(store_id):
    store = request.get_data()
    if "name" not in store or "store_id" not in store:
        abort(400, message = "Ensure that you are sending all the required fields")

    try:
        u_store = stores[store_id]
        u_store |= store

        return u_store
    
    except KeyError:
        abort(404, message= "Store not found")


@app.put('/item/<string:item_id>')
def update_item(item_id):
    store = request.get_data()
    if "price" not in store or "name" not in store or "item_id" not in store:
        abort(400, message = "Ensure that you are sending all the required fields")

    try:
        u_item = item[item_id]
        u_item |= store

        return u_item
    
    except KeyError:
        abort(404, message= "Item not found")


@app.delete('/store/<string:store_id>')
def delete_store(store_id):
    try:
        del stores[store_id]
        return "Store Deleted successfully"
    except KeyError:
        abort(404, message= "Store not found")


@app.delete('/item/<string:item_id>')
def delete_item(item_id):
    try:
        del item[item_id]
        return "Item Deleted successfully"
    
    except KeyError:
        abort(404, message= "Item not found")

    

