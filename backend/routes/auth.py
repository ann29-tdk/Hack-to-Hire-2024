from flask import Blueprint, request, jsonify
from models.user import User
from werkzeug.security import generate_password_hash, check_password_hash
import logging

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    logging.info(f"Register data received: {data}")
    name = data.get('name')
    phoneNumber = data.get('phoneNumber')
    password = data.get('password')
    
    if User.objects(phoneNumber=phoneNumber).first():
        logging.warning(f"User already exists with phone number: {phoneNumber}")
        return jsonify(message='User already exists with this phone number'), 400

    hashed_password = generate_password_hash(password)
    user = User(name=name, phoneNumber=phoneNumber, password=hashed_password, isAdmin=False, associatedFlights=[])
    user.save()
    logging.info(f"User registered successfully: {user}")
    return jsonify(message='User registered successfully'), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    logging.info(f"Login data received: {data}")
    phoneNumber = data.get('phoneNumber')
    password = data.get('password')
    
    if not phoneNumber or not password:
        logging.warning("Phone number and password are required")
        return jsonify(message='Phone number and password are required'), 400

    user = User.objects(phoneNumber=phoneNumber).first()
    if user:
        logging.info(f"User found: {user}")
        if check_password_hash(user.password, password):
            logging.info("Password check successful")
            return jsonify(_id=str(user.id), name=user.name, phoneNumber=user.phoneNumber, isAdmin=user.isAdmin), 200
        else:
            logging.warning("Password check failed")
    else:
        logging.warning(f"User not found with phone number: {phoneNumber}")

    return jsonify(message='Invalid phone number or password'), 400

@auth_bp.route('/user/<user_id>', methods=['GET'])
def get_user(user_id):
    user = User.objects(id=user_id).first()
    if not user:
        return jsonify(message='User not found'), 404
    return jsonify(user), 200

@auth_bp.route('/user/<user_id>/flight', methods=['PUT'])
def update_user_flight(user_id):
    data = request.get_json()
    flightNumber = data.get('flightNumber')
    user = User.objects(id=user_id).first()
    
    if not user:
        return jsonify(message='User not found'), 404

    if flightNumber not in user.associatedFlights:
        user.associatedFlights.append(flightNumber)
        user.save()
    return jsonify(user), 200

@auth_bp.route('/user/<user_id>/notifications/<int:index>', methods=['DELETE'])
def delete_notification(user_id, index):
    user = User.objects(id=user_id).first()
    if not user:
        return jsonify(message='User not found'), 404

    try:
        user.notifications.pop(index)
        user.save()
        return jsonify(message='Notification deleted successfully', user=user), 200
    except IndexError:
        return jsonify(message='Notification index out of range'), 400
