"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for, send_from_directory
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from api.utils import APIException, generate_sitemap
from api.models import db, User

from api.models import User
#from models import Person

ENV = os.getenv("FLASK_ENV")
static_file_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../public/')
app = Flask(__name__)
app.url_map.strict_slashes = False

# database condiguration
db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)

# Allow CORS requests to this API
CORS(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    if ENV == "development":
        return generate_sitemap(app)
    return send_from_directory(static_file_dir, 'index.html')

# any other endpoint will try to serve it like a static file
@app.route('/<path:path>', methods=['GET'])
def serve_any_other_file(path):
    if not os.path.isfile(os.path.join(static_file_dir, path)):
        path = 'index.html'
    response = send_from_directory(static_file_dir, path)
    response.cache_control.max_age = 0 # avoid cache memory
    return response

##### USERS #####
# All users
@app.route('/user', methods=['GET', 'POST'])
def handle_users():
    """
    All Users
    """
    # GET all users
    if request.method == 'GET':
        users = User.query.all()
        all_users = list(map(lambda x: x.serialize(), users))
        return jsonify(all_users), 200

    # Create (POST) a new user
    if request.method == 'POST':
        user_to_add = request.json

        # Data validation
        if user_to_add is None:
            raise APIException("You need to specify the request body as a json object", status_code=400)
        if 'user_name' not in user_to_add:
            raise APIException('You need to specify the username', status_code=400)
        if 'email' not in user_to_add:
            raise APIException('You need to specify the email', status_code=400)
        if 'password' not in user_to_add:
            raise APIException('You need to create a valid password', status_code=400)

        new_user = User(user_name=user_to_add["user_name"], email=user_to_add["email"], password=user_to_add["password"])
        db.session.add(new_user)
        db.session.commit()
        return jsonify(new_user.serialize()), 200

    return "Invalid Method", 404

# Get, Edit or delete a specific user
@app.route('/user/<int:user_id>', methods=['PUT', 'GET', 'DELETE'])
def handle_single_user(user_id):
    """
    Single user
    """
    user = User.query.get(user_id)

    # Data validation
    if user is None:
        raise APIException('User not found in data base', status_code=404)
        
    # Modify (PUT) a user
    if request.method == 'PUT':
        request_body = request.json

        if "user_name" in request_body:
            user.user_name = request_body["user_name"]
        if "email" in request_body:
            user.email = request_body["email"]
        if "password" in request_body:
            user.password = request_body["password"]
        if "is_active" in request_body:
            user.is_active = request_body["is_active"]

        db.session.commit()
        return jsonify(user.serialize()), 200

    # GET a user
    elif request.method == 'GET':
        return jsonify(user.serialize()), 200
    
    # DELETE a user
    elif request.method == 'DELETE':
        # user_planet_list = Fav_planet.query.filter_by(user_id=user_id).first()
        # db.session.delete(user_planet_list)
        db.session.delete(user)
        db.session.commit()
        return "User deleted", 200

    return "Invalid Method", 404

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3001))
    app.run(host='0.0.0.0', port=PORT, debug=True)