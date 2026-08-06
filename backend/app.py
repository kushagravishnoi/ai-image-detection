"""
Main Flask Application for AI Image Detection System
Author: Kushagra Vishnoi
Date: 2026-05-09
"""

import os
import logging
from flask import Flask, jsonify, current_app
from flask_cors import CORS
from datetime import datetime

# Import config and routes robustly so the app can be run both as a module
# (python -m backend.app or via flask with FLASK_APP=backend.app) and as a script
try:
    from backend.config import config
    from backend.routes import api_bp
except Exception:
    from config import config
    from routes import api_bp

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def _str_to_bool(val):
    if isinstance(val, bool):
        return val
    if val is None:
        return False
    return str(val).lower() in ("1", "true", "yes", "on")


def create_app(config_name=None):
    """
    Application factory function
    """
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')

    app = Flask(__name__)

    # Load configuration
    cfg_obj = config.get(config_name, config.get('default'))
    app.config.from_object(cfg_obj)

    # Ensure upload folder exists
    upload_folder = app.config.get('UPLOAD_FOLDER', 'uploads')
    try:
        os.makedirs(upload_folder, exist_ok=True)
    except Exception:
        logger.warning(f"Could not create upload folder: {upload_folder}")

    # Enable CORS
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Register blueprints
    app.register_blueprint(api_bp, url_prefix='/api')

    # Health check endpoint
    @app.route('/health', methods=['GET'])
    def health_check():
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.utcnow().isoformat(),
            'version': '1.0.0'
        }), 200

    # Welcome endpoint
    @app.route('/', methods=['GET'])
    def welcome():
        return jsonify({
            'message': 'AI Image Detection System API',
            'version': '1.0.0',
            'endpoints': {
                'detect': '/api/detect',
                'health': '/health',
                'models': '/api/models',
                'status': '/api/status'
            }
        }), 200

    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Not found'}), 404

    @app.errorhandler(500)
    def internal_error(error):
        logger.error(f'Internal server error: {error}')
        return jsonify({'error': 'Internal server error'}), 500

    logger.info(f'Flask app created with config: {config_name}')
    return app


if __name__ == '__main__':
    config_name = os.getenv('FLASK_ENV', 'development')
    app = create_app(config_name)

    # Determine debug mode reliably
    env_debug = os.getenv('FLASK_DEBUG')
    debug = _str_to_bool(env_debug) if env_debug is not None else app.config.get('DEBUG', False)

    host = os.getenv('FLASK_HOST', '0.0.0.0')
    try:
        port = int(os.getenv('FLASK_PORT', 5000))
    except Exception:
        port = 5000

    app.run(host=host, port=port, debug=debug)
