from schemas.db import db_data

class ItemTagModel(db_data.Model):

    __tablename__ = "item_tags"

    id = db_data.Column(db_data.Integer, primary_key = True)
    item_id = db_data.Column(db_data.Integer, db_data.ForeignKey("items.id"))
    tag_id = db_data.Column(db_data.Integer, db_data.ForeignKey("tags.id"))