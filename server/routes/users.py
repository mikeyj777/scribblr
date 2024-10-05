from flask import Blueprint, request, jsonify
from db import get_user

users_bp = Blueprint('users', __name__)

@users_bp.route('/api/users', methods=['POST'])
def get_user_route():
    try:
        name = request.json['name'].lower()
        user_id = get_user(name)
        return jsonify({"id": user_id, "name": name}), 201
    except KeyError:
        return jsonify({"error": "Name is required"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500