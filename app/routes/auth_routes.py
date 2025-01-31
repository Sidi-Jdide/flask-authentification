from flask import Blueprint, request, jsonify, g
from backend.app.models.user_model import User
from backend.app.utils.jwt_utils import hash_password, check_password, generate_tokens

auth_bp = Blueprint('auth', __name__)

# Route pour l'inscription
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"msg": "Username and password are required"}), 400

    # Vérifier si l'utilisateur existe déjà
    if g.db.query(User).filter_by(username=username).first():
        return jsonify({"msg": "User already exists"}), 409

    # Hasher le mot de passe
    hashed_password = hash_password(password)

    # Créer un nouvel utilisateur
    new_user = User(username=username, password=hashed_password)
    g.db.add(new_user)
    g.db.commit()

    # Générer les tokens JWT
    tokens = generate_tokens(new_user.id)
    return jsonify(access_token=tokens[0], refresh_token=tokens[1]), 201

# Route pour la connexion
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"msg": "Username and password are required"}), 400

    # Vérifier l'utilisateur et le mot de passe
    user = g.db.query(User).filter_by(username=username).first()
    if user and check_password(user.password, password):
        tokens = generate_tokens(user.id)
        return jsonify(access_token=tokens[0], refresh_token=tokens[1]), 200

    return jsonify({"msg": "Bad username or password"}), 401