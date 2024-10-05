from flask import Blueprint, request
from db import create_user

users_bp = Blueprint('users', __name__)

@users_bp.route('/api/users', methods=['POST'])
def create_user_route():
    name = request.json['name'].lower()
    create_user(name)
    return '', 201