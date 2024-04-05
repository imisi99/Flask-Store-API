from schemas.db import db_data

class UserModel(db_data.Model):

    __tablename__ = "users"

    id = db_data.Column(db_data.Integer, primary_key = True)
    username = db_data.Column(db_data.String(50), nullable= False, unique = True)
    email = db_data.Column(db_data.String, nullable= False, unique= True)
    password = db_data.Column(db_data.String(250), nullable = False)