from flask import Blueprint, request, jsonify
from flask_cors import CORS
from db import get_user
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

users_bp = Blueprint('users', __name__)
CORS(users_bp)  # Apply CORS to the users blueprint

@users_bp.route('/api/users', methods=['POST'])
def get_user_route():
    try:
        name = request.json['name'].lower()
        user_id = get_user(name)
        return jsonify({"id": user_id, "name": name}), 201
    except KeyError:
        return jsonify({"error": "Name is required"}), 400
    except Exception as e:
        logging.error(f"Error in get_user_route: {str(e)}")
        return jsonify({"error": str(e)}), 500

# Add an OPTIONS method to handle preflight requests
@users_bp.route('/api/users', methods=['OPTIONS'])
def options_user_route():
    return '', 200