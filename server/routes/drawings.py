from flask import Blueprint, request, jsonify
from db import save_drawing, get_drawings
from utils.image_classifier import classify_image

drawings_bp = Blueprint('drawings', __name__)

@drawings_bp.route('/api/drawings', methods=['POST'])
def save_drawing_route():
    name = request.form['name'].lower()
    image_file = request.files['image']
    predictions = classify_image(image_file)
    save_drawing(name, image_file, predictions)
    return jsonify(predictions), 201

@drawings_bp.route('/api/drawings/<name>', methods=['GET'])
def get_drawings_route(name):
    drawings = get_drawings(name.lower())
    return jsonify(drawings)