from flask import Flask
from flask_cors import CORS


def create_app():
    app = Flask(__name__)
    CORS(app)

    # simple configuration
    app.config['UPLOAD_FOLDER'] = 'uploads'

    from .api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    return app
