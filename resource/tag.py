from flask import Flask
from flask_jwt_extended import jwt_required
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from models import TagModel, ItemModel, StoreModel
from schemas.db import db_data
from schemas.schemas import TagAndItemSchemas, TagSchemas
from sqlalchemy.exc import SQLAlchemyError


blp = Blueprint("tags", __name__, description= "Operation on tags")

@blp.route("/store/<string:store_id>/tag")
class TagsInStore(MethodView):

    @blp.response(200, TagSchemas(many=True))
    def get(self, store_id):
        try:
            tag = db_data.session.query(StoreModel).filter(StoreModel.id == store_id).first()
            if not tag:
                abort(
                    404,
                    message = "Tag not found!"
                )
            
            return tag.tags.all()
        
        except SQLAlchemyError:
            abort(500,
                  message = "An error occured while interacting with the db")
        

    @jwt_required()
    @blp.arguments(TagSchemas)
    @blp.response(201, TagSchemas)
    def post(self, tag_data, store_id):
        try:
            tag = db_data.session.query(TagModel).filter(TagModel.store_id == store_id).filter(TagModel.name == tag_data["name"]).first()
            if tag:
                abort(
                    400,
                    message = "A tag with that name already exist in that store"
                )
            
            new_tag = TagModel(**tag_data, store_id = store_id)

            db_data.session.add(new_tag)
            db_data.session.commit()

            return new_tag
        except SQLAlchemyError as e:
            abort(
                500,
                message = str(e)
            )


@blp.route('/item/<string:item_id>/tag/<string:tag_id>')
class LinkTagsToItem(MethodView):
    @jwt_required()
    @blp.response(201, TagSchemas)
    def post(self, item_id, tag_id):
        item = db_data.session.query(ItemModel).filter(ItemModel.id == item_id).first()
        tag = db_data.session.query(TagModel).filter(TagModel.id == tag_id).first()
        if not item:
            abort(
                404,
                message= "Item not found!"
            )
        if not tag:
            abort(
                404,
                message = "Tag not found!"
            )
        
        item.tags.append(tag)

        try:
            db_data.session.add(item)
            db_data.session.commit()

        except SQLAlchemyError as e :
            abort(500,
                  message= "An error occured while trying to insert tag")
            
        return tag
    
    @jwt_required(fresh= True)
    @blp.response(200, TagAndItemSchemas)
    def delete(self, item_id, tag_id):
        item = db_data.session.query(ItemModel).filter(ItemModel.id == item_id).first()
        tag = db_data.session.query(TagModel).filter(TagModel.id == tag_id).first()

        if not item:
            abort(
                404,
                message = "Item not Found."
            )
        if not tag:
            abort(
                404,
                message = "Tag not Found."
            )

        item.tags.remove(tag)

        try:
            db_data.session.add(item)
            db_data.session.commit()

        except SQLAlchemyError as e:
            print(f"Error occured as {e}")
            abort(500, message= "An error occured while deleting tag from item")

        return {"message" : "Item removed from tag", "item" : item, "tag" : tag}
    

@blp.route('/tag/<string:tag_id>')
class Tag(MethodView):
    @blp.response(200, TagSchemas)
    def get(self, tag_id):
        tag = db_data.session.query(TagModel).filter(TagModel.id == tag_id).first()
        if not tag:
            abort(
                404,
                message = "Tag not found."
            )

        return tag
    

    @jwt_required(fresh= True)
    @blp.response(
        202,
        description= "Deletes a tag if no item is tagged with it.",
        example= {"message": "Tag deleted"}
    )
    @blp.alt_response(404, description= "Tag not found.")
    @blp.alt_response(400,
                      description= "Returned if the tag is assigned to one or more items. In this case, the tag is not deleted due to its Foreign Constraint.")
    
    def delete(self, tag_id):
        tag = db_data.session.query(TagModel).filter(TagModel.id == tag_id).first()

        if not tag:
            abort(
                404,
                message= "Tag not found."
            )

        if not tag.items:
            db_data.session.delete(tag)
            db_data.session.commit()
            return {"message" : "Tag deleted"}
        
        abort(
            400,
            message = "Could not delete tag make sure tag is not associated with any item and then try again"
        )