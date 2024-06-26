from flask import Flask, jsonify
from flask_mail import Mail, Message
from flask import current_app
import os
from flask_smorest import Blueprint, abort
from flask.views import MethodView
from schemas.schemas import UserSchemas, UserRegisterSchema
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
from rq import Queue
import redis
from task import send_simple_message, send_user_registration_email

blp = Blueprint("users", __name__, description= "Operating on users")




@blp.route('/user/register')
class Signup(MethodView):
    @blp.arguments(UserRegisterSchema)
    @blp.response(201)   
    def post(self, user_data):
        try:
            user = db_data.session.query(UserModel).filter(UserModel.username == user_data["username"]).first()
            email = db_data.session.query(UserModel).filter(UserModel.email == user_data["email"]).first()
            if user:
                abort(
                    409,
                    message= "An account with that username already exists"
                )

            if email:
                abort(
                    409,
                    message = "An account with that email already exists"
                )
            

            data = UserModel(
                username = user_data["username"],
                email = user_data["email"],
                password = pbkdf2_sha256.hash(user_data["password"])
            )
            db_data.session.add(data)
            db_data.session.commit()

            
            current_app.queue.enqueue(send_user_registration_email, data.email, data.username)

            send_simple_message(
                to= data.email,
                subject= "Successfully Signed up!",
                body= f"Hi {data.username} you have successfully signed up to the Stores API"
            )
            return "Account has been ccreated successfully, check your mail for verification!"
            # try:
            #     msg = Message(
            #         'Hello',
            #         sender= "isongrichard234@gmail.com",
            #         recipients= [data.email]
            #     )
            #     msg.body = f"Hello {data.username}, We are glad to have you on board with us on this journey. Congratulations on Signing up for the Stores API"
            #     with current_app.app_context():
            #         current_app.extensions['mail'].send(msg)
            #     return "Account has been ccreated successfully, check your mail for verification!"
            # except Exception as e:
            #     return jsonify({"message": "Failed to send email!","error": str(e)}), 500

           
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
            current_user_id = get_jwt_identity()

            if user_id != current_user_id:
                abort(
                    403,
                    message = "Access Denied!"

                )
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
            current_user_id = get_jwt_identity()

            if user_id != current_user_id:
                abort(
                    403,
                    message = "Access Denied!"
                )

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
        