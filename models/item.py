from schemas.db import db_data

class ItemModel(db_data.Model):

    __tablename__ = "items"

    id = db_data.Column(db_data.Integer, primary_key= True)
    name = db_data.Column(db_data.String(50), nullable= False, unique= True)
    price = db_data.Column(db_data.Float(precision=2), nullable = False)
    store_id = db_data.Column(db_data.Integer, db_data.ForeignKey("stores.id"), nullable= False)
    
    store = db_data.relationship("StoreModel", back_populates= "items")

    tags = db_data.relationship("TagModel", back_populates= "items", secondary= "item_tags")