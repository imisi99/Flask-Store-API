from db import db_data

class StoreModel(db_data.Model):
    __tablename__ = "stores"
    id = db_data.Column(db_data.Integer, primary_key= True)
    name = db_data.Column(db_data.String(50), nullable= False, unique= True)