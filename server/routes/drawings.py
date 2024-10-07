from flask import Blueprint, request, jsonify, current_app
from flask_cors import CORS
from db import save_drawing, get_drawings
# from utils.image_classifier import classify_image

import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

drawings_bp = Blueprint('drawings', __name__)
CORS(drawings_bp)

@drawings_bp.record
def record_params(setup_state):
    app = setup_state.app
    drawings_bp.config = app.config
    
@drawings_bp.route('/api/drawings', methods=['POST'])
def save_drawing_route():
    user_id = request.form['userId']
    image_file = request.files['image']
    # predictions = classify_image(image_file)
    predictions = ['dummy prediction']
    drawing_id = save_drawing(user_id, image_file, predictions)
    return jsonify({
        "id": drawing_id,
        "image_path": f"uploads/{drawing_id}.jpg",
        "predictions": predictions
    }), 201

@drawings_bp.route('/api/drawings/<int:user_id>', methods=['GET'])
def get_drawings_route(user_id):
    drawings = get_drawings(user_id)
    return jsonify(drawings)