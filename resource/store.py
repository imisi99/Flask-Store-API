from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas.schemas import StoreSchemas
from models import StoreModel
from schemas.db import db_data
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

blp = Blueprint("stores", __name__, description= "Operations on stores")

@blp.route('/store/<string:store_id>')
class Store(MethodView):
    @blp.response(200, StoreSchemas)
    def get(self, store_id):
        #store = StoreModel.query.get_or_404(store_id)
            try:
                store = db_data.session.query(StoreModel).filter(StoreModel.id == store_id).first()
                if store is not None:
                    return store
                abort(404,
                    message= "Store not found")
            
            except SQLAlchemyError:
                 abort(500,
                       message= "An error occured while retrieving the data!")



    def delete(self, store_id):
            try:
                store = db_data.session.query(StoreModel).filter(StoreModel.id == store_id).first()
                if store is not None:
                    db_data.session.delete(store)
                    db_data.session.commit()
                    return "Store has been deleted"
                
                abort(404,
                      message= "Store not found")

            except SQLAlchemyError:
                abort(500,
                       message= "An error occured while deleting the data!")

            



    @blp.arguments(StoreSchemas)
    @blp.response(201)
    def put(self,store_data, store_id):
        try:
            store = db_data.session.query(StoreModel).filter(StoreModel.id == store_id).first()
            if store is not None:
                store.name = store_data["name"]
                db_data.session.add(store)
                db_data.session.commit()
                return "Store has been updated"
            
            abort(404,
                  message = "Store not found")
        
        except IntegrityError:
            abort(400,
                  message= "A store with that name already exists!")
            
        except SQLAlchemyError:
            abort(500, 
                  message= "An error occured while trying to update data!")



@blp.route('/store')
class StoreList(MethodView):
    @blp.response(200, StoreSchemas(many= True))
    def get(self):
        try:
            store = db_data.session.query(StoreModel).all()
            if store is not None:
                return store
            return "No store has been created"
        
        except SQLAlchemyError:
            abort(500,
                  message= "An error occured while trying to retrieve the data!")

    @blp.arguments(StoreSchemas)
    @blp.response(201, StoreSchemas)
    def post(self, store_data):
        store = StoreModel(**store_data)
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
    


