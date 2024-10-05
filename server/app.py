from flask import Flask
from flask_cors import CORS
from routes.users import users_bp
from routes.drawings import drawings_bp

import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["http://scribble.riskspace.net", "http://localhost:3000"]}})
app.register_blueprint(users_bp)
app.register_blueprint(drawings_bp)

if __name__ == '__main__':
    app.run()