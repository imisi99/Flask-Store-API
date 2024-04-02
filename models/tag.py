from schemas.db import db_data

class TagModel(db_data.Model):
    __tablename__ = "tags"

    id = db_data.Column(db_data.Integer, primary_key = True)
    name = db_data.Column(db_data.String(50), nullable=False, unique = True)
    store_id = db_data.Column(db_data.Integer, db_data.ForeignKey("stores.id"), nullable= False)

    store = db_data.relationship("StoreModel", back_populates= "tags")