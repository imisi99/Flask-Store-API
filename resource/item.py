from flask import request
from flask_jwt_extended import jwt_required
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from models import ItemModel
from schemas.db import db_data
from schemas.schemas import ItemSchemas, ItemUpdateSchemas
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

blp = Blueprint("items", __name__, description= "Operating on items")

@blp.route('/item/<string:item_id>')
class List(MethodView):
    @blp.response(200, ItemSchemas)
    def get(self, item_id):
        try:
            item = db_data.session.query(ItemModel).filter(ItemModel.id == item_id).first()
            if item is not None:
                return item
            else:
                abort(
                    404,
                    message= "Item not found!"
                )
            
        except SQLAlchemyError:
            abort(500,
                  message = "An error occured while trying to fetch data from the database")


    @jwt_required()
    @blp.arguments(ItemUpdateSchemas)
    @blp.response(201, ItemSchemas)
    def put(self, data, item_id):
        try:
            item = db_data.session.query(ItemModel).filter(ItemModel.id == item_id).first()
            if item is None:
                abort(
                    404,
                    message = "Item not found!"
                )
            else:
                item.name = data["name"]
                item.price = data["price"]

                db_data.session.add(item)
                db_data.session.commit()

                return item
        except SQLAlchemyError:
            abort(500,
                message= "An error occured while trying to update the data!")

    @jwt_required(fresh= True)
    def delete(self, item_id):
            try:
                item = db_data.session.query(ItemModel).filter(ItemModel.id == item_id).first()
                if item is None:
                    abort(
                        404,
                        message= "Item not found!"
                    )
                
                else:
                    db_data.session.delete(item)
                    db_data.session.commit()

                    return "Item has been deleted successfully!"
                
            except SQLAlchemyError:
                abort(500,
                      message = "An error occured while trying to delete the data")



@blp.route('/item')
class ItemList(MethodView):
    @blp.response(200, ItemSchemas(many= True))
    def get(self):
        item = db_data.session.query(ItemModel).all()
        if item is not None:
            return item
        return "There are no items in the db"
    
    @jwt_required()
    @blp.arguments(ItemSchemas)
    @blp.response(201, ItemSchemas)
    def post(self, data):
        item = ItemModel(**data)

        try:
            db_data.session.add(item)
            db_data.session.commit()

        except IntegrityError:
            abort(400, message= "An item with that name already exists!")
        
        except SQLAlchemyError as e :
            print(f"The error that occured was: {e}")
            abort(500,
                   message= "An error occured while creating the item")

        return item
    