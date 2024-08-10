"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import request, jsonify, url_for, Blueprint, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from api.models import db, User
from api.utils import generate_sitemap, APIException
from api.utils import generate_token, verify_token
from flask_cors import CORS

api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)


@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():
    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }
    return jsonify(response_body), 200

@api.route('/signup', methods=['POST'])
def signup():
    
    data = request.json
    if 'email' not in data or 'password' not in data:
        return jsonify({"error": "Email and password required"}), 400
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({"error": "User already exists"}), 400
    
    new_user = User(email=data['email'])
    new_user.set_password(data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User created successfully"}), 201

@api.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
     # Buscar el usuario por email

    # Aquí verifica si el email y la contraseña son correctos
    user = User.query.filter_by(email=email).first()

    if user and check_password_hash(user.password_hash, password):
        # Autenticación exitosa
        access_token = create_access_token(identity=user.id)
        return jsonify(token=access_token, message="Login successful"), 200
    else:
        # Credenciales inválidas
        return jsonify({"message": "Invalid credentials"}), 401

# @api.route('/logout', methods=['POST'])
# def logout():
#     session.pop('user_id', None)
#     return jsonify({"message": "Logged out successfully"}), 200

@api.route('/private', methods=['GET'])
@jwt_required()
def private():
    current_user = get_jwt_identity()  # Obtiene la identidad del usuario desde el token
    return jsonify({"message": f"This is a private route for user {current_user}"}), 200

@api.route('/validate-token', methods=['POST'])
def validate_token():
    token = request.headers.get('Authorization')
    if verify_token(token):
        return jsonify({"message": "Token is valid"}), 200
    return jsonify({"message": "Token is invalid"}), 401