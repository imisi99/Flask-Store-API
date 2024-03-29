import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import StoreSchema
from models import StoreModel
from db import db_data
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

blp = Blueprint("stores", __name__, description= "Operations on stores")

@blp.route('/store/<string:store_id>')
class Store(MethodView):
    @blp.response(200, StoreSchema)
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


    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def put(self,store_data, store_id):
        try:
            u_store = stores[store_id]
            u_store |= store_data

            return u_store
        
        except KeyError:
            abort(404, message= "Store not found")



@blp.route('/store')
class StoreList(MethodView):
    @blp.response(200, StoreSchema(many= True))
    def get(self):
        return stores.values()
    

    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self, store_data):
        store = Store(**store_data)
        try:
            db_data.session.add(store)
            db_data.session.commit()
        
        except IntegrityError:
            abort(
                400,
                message= "A store with that name already exists"
            )
        
        except SQLAlchemyError as e :
            print(f"The error that occured was :{e}")
            abort(
                500,
                message= "An error occured while creating the store"
            )
        return store
    


