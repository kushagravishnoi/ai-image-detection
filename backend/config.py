"""
Configuration settings for Flask application
"""

import os
from datetime import timedelta

class Config:
    """
    Base configuration
    """
    # Flask settings
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # File upload settings
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50MB max file size
    UPLOAD_FOLDER = 'uploads'
    ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'bmp', 'webp'}
    
    # Model settings
    MODEL_PATH = 'models/pretrained'
    DEFAULT_MODEL = 'cnn_detector_v1.h5'
    CONFIDENCE_THRESHOLD = 0.5
    
    # API settings
    JSON_SORT_KEYS = False
    JSONIFY_PRETTYPRINT_REGULAR = True
    
    # Database (if using)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    
    # CORS settings
    CORS_ORIGINS = ['http://localhost:3000', 'http://localhost:5000']

class DevelopmentConfig(Config):
    """
    Development configuration
    """
    DEBUG = True
    TESTING = False
    ENV = 'development'
    SQLALCHEMY_ECHO = True

class TestingConfig(Config):
    """
    Testing configuration
    """
    TESTING = True
    DEBUG = True
    ENV = 'testing'
    DATABASE_URL = 'sqlite:///:memory:'
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10MB for testing

class ProductionConfig(Config):
    """
    Production configuration
    """
    DEBUG = False
    TESTING = False
    ENV = 'production'
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_ECHO = False
    # Additional security settings for production
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
