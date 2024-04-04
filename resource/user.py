from flask import Flask
from flask_smorest import Blueprint, abort
from flask.views import MethodView
from schemas.schemas import UserSchemas
from models import UserModel
from sqlalchemy.exc import SQLAlchemyError
from schemas.db import db_data
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt,
    get_jwt_identity
)
from blocklist import BLOCKLIST

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
                    409,
                    message= "An account with that username already exists"
                )
            

            data = UserModel(
                username = user_data["username"],
                password = pbkdf2_sha256.hash(user_data["password"])
            )

            db_data.session.add(data)
            db_data.session.commit()

            return {"message" : "Account has been created successfully!"}, 201
        
        except SQLAlchemyError:
            abort(500,
                  message = "An error occured while pushing data to the database")
            

@blp.route('/user/login')
class Login(MethodView):
    @blp.arguments(UserSchemas)
    @blp.response(201)
    def post(self, user_data):
        try:
            user = db_data.session.query(UserModel).filter(UserModel.username == user_data["username"]).first()
            if user and pbkdf2_sha256.verify(user_data["password"], user.password):
                access_token = create_access_token(identity= user.id, fresh= True)
                refresh_token = create_refresh_token(user.id)
                return {"access_token" : access_token, "refresh_token" : refresh_token}, 200
            
            abort(401, 
                  message = "Invalid credentials.")
            
        except SQLAlchemyError:
            abort(500,
                  message = "An error occured while trying to log in try again later!")


@blp.route('/user/logout')
class Logout(MethodView):
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"message" : "Successfully logged out "}, 200



@blp.route('/user/<int:user_id>')
class User(MethodView):
    @jwt_required(fresh= True)
    @blp.response(200, UserSchemas)
    def get(self, user_id):
        try:
            user = db_data.session.query(UserModel).filter(UserModel.id == user_id).first()
            if not user:
                abort(
                    404,
                    message = "User not found!"
                )
            
            return user
        
        except SQLAlchemyError:
            abort(500,
                  message = "An error occured while trying to get data from the db!")
            
    @jwt_required(fresh= True)
    def delete(self, user_id):
        try:
            user = db_data.session.query(UserModel).filter(UserModel.id == user_id).first()
            if not user:
                abort(
                    404,
                    message = "User not found!"
                )
            
            db_data.session.delete(user)
            db_data.session.commit()

            return {"message" : "User has been deleted successfully"}
        
        except SQLAlchemyError:
            abort(500,
                  message = "An error occured while Interacting with the db!")
            


@blp.route('/user/refresh')
class TokenRefresh(MethodView):
    @jwt_required(refresh= True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh= False)

        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"access_token" : new_token}, 200
        