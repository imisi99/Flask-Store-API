import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from models import ItemModel
from db import db_data
from schemas import Itemschemas, ItemUpdateSchemas
from sqlalchemy.exc import SQLAlchemyError

blp = Blueprint("items", __name__, description= "Operating on items")

@blp.route('/item/<string:item_id>')
class List(MethodView):
    @blp.response(200, Itemschemas)
    def get(self, item_id):
        try:
            return item[item_id], 200
        except KeyError:
            abort(404, message = "Item not found.")



    @blp.arguments(ItemUpdateSchemas)
    @blp.response(201, Itemschemas)
    def put(self, item_data, item_id):
        try:
            u_item = item[item_id]
            u_item |= item_data

            return u_item
        
        except KeyError:
            abort(404, message= "Item not found")

    
    def delete(self, item_id):
            try:
                del item[item_id]
                return "Item Deleted successfully"
            
            except KeyError:
                abort(404, message= "Item not found")


@blp.route('/item')
class ItemList(MethodView):
    @blp.response(200, Itemschemas(many= True))
    def get(self):
        return item.values()
    

    @blp.arguments(Itemschemas)
    @blp.response(201, Itemschemas)
    def post(self, data):
        item = Item(**data)

        try:
            db_data.session.add(item)
            db_data.session.commit()
        
        except SQLAlchemyError:
            abort(500, message= "An error occured while collecting data, Please try again later")
        return item
    