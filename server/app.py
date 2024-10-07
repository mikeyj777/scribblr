import os

from flask import Flask
from flask_cors import CORS
from routes.users import users_bp
from routes.drawings import drawings_bp

import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def create_app():
    app = Flask(__name__)
    
    # Set the upload folder
    app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'uploads')
    
    # Ensure the upload folder exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Apply CORS configuration
    CORS(app, resources={r"/*": {"origins": ["http://scribble.riskspace.net", "http://localhost:3000"]}}, supports_credentials=True)

    # Register blueprints
    app.register_blueprint(drawings_bp)
    app.register_blueprint(users_bp)  # Uncomment this line
    
    return app

if __name__ == '__main__':
    # If you're using the app factory pattern:
    app = create_app()
    app.run(debug=True)