from flask import Flask
from flask_smorest import Blueprint, abort
from flask.views import MethodView
from schemas.schemas import UserSchemas
from models import UserModel
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from schemas.db import db_data

blp = Blueprint("users", __name__, description= "Operating on users")

@blp.route('/user/register')
class Signup(MethodView):
    @blp.arguments(UserSchemas)
    @blp.response(201)   
    def post(self, user_data):
        try:
            user = db_data.session.query(UserModel).filter(UserModel.username == user_data["username"]).first()
            if user:
                abort(
                    400,
                    message= "An account with that username already exists"
                )
            

            data = UserModel(**user_data)

            db_data.session.add(data)
            db_data.session.commit()
            return "Account has been created successfully!"
        
        except SQLAlchemyError:
            abort(500,
                  message = "An error occured while pushing data to the database")


