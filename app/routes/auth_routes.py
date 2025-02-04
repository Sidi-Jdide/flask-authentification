from flask import Blueprint, request, jsonify, g
from ..models.user_model import User
from ..utils.jwt import hash_password, check_password, generate_tokens
from flask_jwt_extended import jwt_required, get_jwt_identity

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Bad Request", "message": "No data provided"}), 400

    required_fields = ['username', 'password']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": "Bad Request", "message": f"Missing field: {field}"}), 400

    username = data.get('username')
    password = data.get('password')

    if g.db.query(User).filter_by(User.username==username).first():
        return jsonify({"error": "Conflict", "message": "User already exists"}), 409

    hashed_password = hash_password(password)

    new_user = User(username=username, password=hashed_password)
    g.db.add(new_user)
    g.db.commit()

    tokens = generate_tokens(new_user.id)
    return jsonify(access_token=tokens[0], refresh_token=tokens[1]), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Bad Request", "message": "No data provided"}), 400

    required_fields = ['username', 'password']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": "Bad Request", "message": f"Missing field: {field}"}), 400

    username = data.get('username')
    password = data.get('password')


    user = g.db.query(User).filter(username==username).first()
    if user and check_password(user.password, password):
        tokens = generate_tokens(user.id)
        return jsonify(access_token=tokens[0], refresh_token=tokens[1]), 200

    return jsonify({"error": "Unauthorized", "message": "Bad username or password"}), 401

@auth_bp.route('/protected', methods=['GET'])
@jwt_required()
def protected():
        # Récupérer l'identité de l'utilisateur à partir du token JWT
        current_user = get_jwt_identity()
        return jsonify(logged_in_as=current_user), 200