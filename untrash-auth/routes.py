from enum import auto
from flask import Blueprint, request, jsonify, session
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from .models import db, User
from models import db, User


auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if User.query.filter_by(email=email).first():
        return jsonify({"msg": "User already exists"}), 409

    user = User(email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({"msg": "User created"}), 201

@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    if user and user.check_password(password):
        session['user_id'] = user.id
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token, session_id=session.sid), 200
    return jsonify({"msg": "Bad email or password"}), 401

@auth.route('/check_session', methods=['GET'])
def check_session():
    user_id = session.get('user_id')
    if user_id:
        return jsonify({"msg": "Session active", "user_id": user_id}), 200
    return jsonify({"msg": "Session not found"}), 404

@auth.route('/extend_session', methods=['POST'])
def extend_session():
    session.permanent = True
    return jsonify({"msg": "Session extended"}), 200

@auth.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user_id = get_jwt_identity()
    return jsonify({"msg": f"Hello user {current_user_id}"}), 200
