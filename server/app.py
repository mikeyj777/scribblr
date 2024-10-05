from flask import Flask
from flask_cors import CORS
from routes.users import users_bp
from routes.drawings import drawings_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(users_bp)
app.register_blueprint(drawings_bp)

if __name__ == '__main__':
    app.run()