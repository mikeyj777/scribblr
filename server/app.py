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
    
    logging.debug(f"Upload folder: {app.config['UPLOAD_FOLDER']}")

    # Ensure the upload folder exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    app.register_blueprint(drawings_bp)
    app.register_blueprint(users_bp)
    
    # Other app configurations and blueprints registration go here
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": ["http://scribble.riskspace.net", "http://localhost:3000"]}})
    app.register_blueprint(users_bp)
    app.register_blueprint(drawings_bp)
    
    return app

# If you're using the app factory pattern:
app = create_app()

if __name__ == '__main__':
    app.run()