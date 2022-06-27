"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User
from api.utils import generate_sitemap, APIException
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required

api = Blueprint('api', __name__)



@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "message": "Hello User!. Please insert your e-mail and Password to go in!"
    }

    return jsonify(response_body), 200



# Create a route to authenticate your users and return JWT Token. The
# create_access_token() function is used to actually generate the JWT.
@api.route('/token', methods=["POST"])
def create_token():
    email_recieved = request.json.get("email", None)
    password_recieved = request.json.get("password", None)
    # Query your database for username and password
    user = User.query.filter_by(email=email_recieved, password=password_recieved).first()
    if user is None:
        # the user was not found on the database
        return jsonify({"msg": "There is no this e-mail in the database"}), 401
    
    # create a new token with the user id inside
    access_token = create_access_token(identity=user.id)
    return jsonify({ "token": access_token, "user_id": user.id })


@api.route('/signup', methods=["POST"])
def create_user():
    email_recieved = request.json.get("email", None)
    password_recieved = request.json.get("password", None)
  
  # we look for an email repeated
    email_repited = User.query.filter_by(email=email_recieved).first()
    if email_repited != None:
        return jsonify({"show" : True , "text" : "This user is already created, please, insert another email!"}),400
    
    # there is no email or password
    if email_recieved =='' or password_recieved == '':
        return jsonify({ "show" : True , "text": "Email and password are necessary" }), 401

      # Query your database for username and password
    new_user = User(email = email_recieved,password = password_recieved , is_active= False)
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({ "show" : True , "text" : "User Created !"}),200
    