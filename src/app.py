import os
from flask import Flask, jsonify, send_from_directory
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from api.models import db
from api.routes import api
from api.admin import setup_admin
from api.commands import setup_commands
from api.utils import APIException, generate_sitemap

# -------------------------
# Flask App Initialization
# -------------------------
app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "https://turbo-waddle-g4rg4gj997vw2v7q7-3000.app.github.dev"}})

# Database config
db_url = os.getenv("DATABASE_URL")
if db_url:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///test.db"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["JWT_SECRET_KEY"] = "super-secret-key"

# -------------------------
# Extensions
# -------------------------
db.init_app(app)
Migrate(app, db, compare_type=True)
jwt = JWTManager(app)

# -------------------------
# Blueprints & Admin
# -------------------------
app.register_blueprint(api, url_prefix="/api")
setup_admin(app)
setup_commands(app)

# -------------------------
# Error handling
# -------------------------
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# -------------------------
# Static file / sitemap
# -------------------------
ENV = "development" if os.getenv("FLASK_DEBUG") == "1" else "production"
static_file_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../dist/')

@app.route('/')
def sitemap():
    if ENV == "development":
        return generate_sitemap(app)
    return send_from_directory(static_file_dir, 'index.html')

@app.route('/<path:path>', methods=['GET'])
def serve_any_other_file(path):
    if not os.path.isfile(os.path.join(static_file_dir, path)):
        path = 'index.html'
    response = send_from_directory(static_file_dir, path)
    response.cache_control.max_age = 0
    return response

# -------------------------
# Run server
# -------------------------
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3001))
    app.run(host='0.0.0.0', port=PORT, debug=True)
