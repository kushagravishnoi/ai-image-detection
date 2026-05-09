"""
Main Flask Application for AI Image Detection System
Author: Kushagra Vishnoi
Date: 2026-05-09
"""

import os
import logging
from flask import Flask, jsonify
from flask_cors import CORS
from datetime import datetime

from config import config
from routes import api_bp

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_app(config_name='development'):
    """
    Application factory function
    """
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
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
    app = create_app(os.getenv('FLASK_ENV', 'development'))
    app.run(
        host=os.getenv('FLASK_HOST', '0.0.0.0'),
        port=int(os.getenv('FLASK_PORT', 5000)),
        debug=os.getenv('FLASK_DEBUG', True)
    )
